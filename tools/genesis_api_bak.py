# 后端创世引擎

import os
# 强制拔掉 Mem0 遥测，世界清净
os.environ["MEM0_TELEMETRY"] = "false"
import json
import sys
import warnings
import re
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from colorama import init, Fore
from dotenv import load_dotenv
import httpx

from mem0 import Memory
from neo4j import GraphDatabase
from neo4j.warnings import Neo4jWarning
from openai import OpenAI

init(autoreset=True)
warnings.filterwarnings("ignore", category=Neo4jWarning)

# ==========================================
# 0. 环境感知与防御性校验
# ==========================================
load_dotenv()

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USER")
NEO4J_PASS = os.environ.get("NEO4J_PASS")
API_KEY = os.environ.get("ZHIPU_API_KEY")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

# 致命变量缺失检查（Fail-Fast 机制）
missing_vars = []
if not NEO4J_URI: missing_vars.append("NEO4J_URI")
if not NEO4J_USER: missing_vars.append("NEO4J_USER")
if not NEO4J_PASS: missing_vars.append("NEO4J_PASS")
if not API_KEY: missing_vars.append("ZHIPU_API_KEY")

if missing_vars:
    print(Fore.RED + f"[致命错误] 拒绝启动！缺少环境变量: {', '.join(missing_vars)}")
    sys.exit(1)

app = FastAPI(title="ZiJin Genesis Lab API", version="1.3")

# ==========================================
# 1. 核心基础设施连接池
# ==========================================
neo4j_driver = None
mem0 = None
llm_client = None
try:
    # Neo4j图谱连接
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    neo4j_driver.verify_connectivity()

    # 将环境变量注入OS，以便Mem0底层能够无缝读取
    os.environ["OPENAI_API_KEY"] = API_KEY
    os.environ["OPENAI_BASE_URL"] = BASE_URL

    # Mem0向量记忆连接
    mem0 = Memory.from_config({
        "llm": {"provider": "openai", "config": {"model": "glm-4"}},
        "embedder": {"provider": "openai", "config": {"model": "embedding-3"}},
        "vector_store": {"provider": "chroma", "config": {"collection_name": "zijin_episodic", "path": "./.mem0_db"}}
    })

    # 大模型抽取中枢
    llm_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    print(Fore.GREEN + "[系统自检] 创世基础设施 (Neo4j, Mem0, LLM) 连接成功。")
except Exception as e:
    print(Fore.RED + f"[系统自检] 致命错误，基础设施连接失败: {e}")
    sys.exit(1)


# ==========================================
# 2. Pydantic数据模型
# ==========================================
class DialogueLine(BaseModel):
    speaker: str
    content: str

class SceneData(BaseModel):
    scene_id: str
    timestamp: str
    context: str
    dialogues: List[DialogueLine]

class CreatorInfo(BaseModel):
    user_id: str
    nickname: str
    role: str = "Creator"

# ==========================================
# 3. 核心路由与接口
# ==========================================

@app.get("/api/status")
async def check_system_status():
    """检查系统是否已被唤醒（图谱中是否存在Creator）"""
    with neo4j_driver.session() as session:
        result = session.run("MATCH (c:Person {role: 'Creator'}) RETURN c.user_id AS user_id")
        record = result.single()
        if record:
            return {"status": "awakened", "creator_id": record["user_id"]}
        return {"status": "dormant", "message": "记忆扇区空白，等待造物主唤醒。"}


@app.post("/api/bind_creator")
async def bind_creator(info: CreatorInfo):
    """锚定造物主实体"""
    try:
        with neo4j_driver.session() as session:
            # 强行创建或合并造物主节点，并设置全局唯一user_id
            session.run("""
                MERGE (c:Person {user_id: $user_id})
                SET c.name = $nickname, c.role = $role
            """, user_id=info.user_id, nickname=info.nickname, role=info.role)
        return {"status": "success", "message": f"成功锚定造物主：{info.nickname} ({info.user_id})"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图谱写入失败: {e}")


# 异步后台任务逻辑
def process_knowledge_injection(scene: SceneData, creator_id: str):
    """后台抽取与落盘逻辑"""
    print(Fore.YELLOW + f" -> 正在处理场景: {scene.scene_id}")

    prompt = f"""
    你是一个严谨的知识提取引擎。请提取以下对话的图谱关系和情景摘要：
    1. 'graph_relations': 提取事实三元组，格式 [["实体1", "关系", "实体2"]]。
    2. 'episodic_summary': 站在ZiJin的第一人称视角，写50字以内的一句话摘要。
    输入数据：{scene.model_dump_json()}
    """

    try:
        # 1. 大模型提取
        response = llm_client.chat.completions.create(
            model="glm-4-flash-250414",
            messages=[
                {"role": "system", "content": "必须输出严格的JSON。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        # 查看大模型生成
        raw_content = response.choices[0].message.content
        print(Fore.LIGHTBLACK_EX + f"    [LLM 原始截取输出] {raw_content[:100]}...")
        # 处理可能被Markdown格式包裹的JSON
        # 使用正则表达式暴力提取JSON对象
        match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if not match:
            print(Fore.RED + f"    ❌ 无法从大模型输出中匹配到JSON结构体。")
            return

        clean_json_str = match.group(0)

        try:
            data = json.loads(clean_json_str)
        except json.JSONDecodeError as je:
            print(Fore.RED + f"    ❌ JSON 格式严重损毁: {je}")
            print(Fore.RED + f"    损毁内容: {clean_json_str}")
            return

        relations = data.get("graph_relations", [])
        summary = data.get("episodic_summary", "")

        # 2. 图谱落盘(Neo4j)
        if relations:
            with neo4j_driver.session() as session:
                for rel in relations:
                    if len(rel) == 3:
                        session.run("""
                        MERGE (s:Entity {name: $subj})
                        MERGE (o:Entity {name: $obj})
                        MERGE (s)-[:RELATION {type: $pred}]->(o)
                        """, subj=rel[0], pred=rel[1], obj=rel[2])
            print(Fore.GREEN + f"    ✅ Neo4j: 写入 {len(relations)} 条关系。")

        # 3. 向量落盘(Mem0)
        if summary:
            # 强制绑定之前注册的creator_id
            mem0.add(summary, user_id=creator_id, metadata={"scene_id": scene.scene_id})
            print(Fore.GREEN + f"    ✅ Mem0: 摘要已压入 -> {summary[:20]}...")

    except Exception as e:
        print(Fore.RED + f"    ❌ 处理场景 {scene.scene_id} 时发生异常: {e}")


@app.post("/api/memory/inject")
async def inject_memory(scenes: List[SceneData], background_tasks: BackgroundTasks):
    """接收大量聊天记录，并放入后台队列慢慢处理，不阻塞前端"""
    # 必须先确认系统已绑定Creator
    with neo4j_driver.session() as session:
        result = session.run("MATCH (c:Person {role: 'Creator'}) RETURN c.user_id AS user_id")
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="请先调用/api/bind_creator！")
        creator_id = record["user_id"]

    # 将任务推入FastAPI的后台任务队列
    for scene in scenes:
        background_tasks.add_task(process_knowledge_injection, scene, creator_id)

    return {"status": "processing", "message": f"已接收 {len(scenes)} 个场景，正在后台提取向量与图谱..."}


if __name__ == "__main__":
    print(Fore.CYAN + "正在启动ZiJin创世后台服务...")
    # 启动ASGI服务器，监听8000端口
    uvicorn.run("genesis_api:app", host="127.0.0.1", port=8000, reload=True)