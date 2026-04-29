import os
import sys

# 设定标准输出编码为UTF-8以免Windows控制台打印emoji崩溃
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import re
import shutil
from fastapi import FastAPI, File, UploadFile, Body, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from colorama import init, Fore, Style
from mem0 import Memory
from neo4j import GraphDatabase

init(autoreset=True)

app = FastAPI(title="ZiJin Genesis Core")

# Mem0全局单例（懒加载，等配置就绪后首次调用时初始化）
_mem0_client = None

def get_mem0_client():
    """获取Mem0单例，避免重复创建导致Qdrant锁冲突"""
    global _mem0_client
    if _mem0_client is None:
        # 确保环境变量已就绪
        if not os.getenv("OPENAI_API_KEY") and os.getenv("LLM_API_KEY"):
            os.environ["OPENAI_API_KEY"] = os.getenv("LLM_API_KEY")
        if not os.getenv("OPENAI_BASE_URL") and os.getenv("LLM_BASE_URL"):
            os.environ["OPENAI_BASE_URL"] = os.getenv("LLM_BASE_URL")

        llm_model = os.getenv("LLM_MODEL", "glm-4-flash")
        embedding_model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")

        # 如果是embedding-开头就算openai供应商，其余暂作huggingface开源本地处理
        embedder_provider = "openai" if embedding_model.startswith("embedding-") else "huggingface"

        print(Fore.CYAN + "  [潜意识初始化] 正在连接Mem0向量深渊...")
        config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": llm_model,
                }
            },
            "embedder": {
                "provider": embedder_provider,
                "config": {
                    "model": embedding_model
                }
            },
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "zijin_episodic_local",
                    "path": "./.mem0_db"
                }
            }
        }
        _mem0_client = Memory.from_config(config)
    return _mem0_client


# 允许前端跨域请求(CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 1. 灵枢：环境变量覆写接口
# ==========================================
class EnvConfig(BaseModel):
    LLM_MODEL: str
    EMBEDDING_MODEL: str
    LLM_BASE_URL: str
    LLM_API_KEY: str
    CREATOR_QQ: str
    NAPCAT_TOKEN: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASS: str


@app.post("/api/config/save")
async def save_config(config: EnvConfig):
    print(Fore.CYAN + "\n[灵枢运转] 接收到高维空间的环境配置注入...")
    # 将配置文件写入项目根目录 (tools的上级目录)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, ".env")

    # .env覆写
    env_content = f"""# ZiJin Auto-Generated Config
LLM_MODEL={config.LLM_MODEL}
EMBEDDING_MODEL={config.EMBEDDING_MODEL}
LLM_BASE_URL={config.LLM_BASE_URL}
LLM_API_KEY={config.LLM_API_KEY}
CREATOR_QQ={config.CREATOR_QQ}
QQ_ACCESS_TOKEN={config.NAPCAT_TOKEN}
NEO4J_URI={config.NEO4J_URI}
NEO4J_USER={config.NEO4J_USER}
NEO4J_PASS={config.NEO4J_PASS}
"""
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    # 动态应用到当前进程
    os.environ["LLM_BASE_URL"] = config.LLM_BASE_URL
    os.environ["LLM_API_KEY"] = config.LLM_API_KEY
    os.environ["CREATOR_QQ"] = config.CREATOR_QQ
    os.environ["OPENAI_API_KEY"] = config.LLM_API_KEY
    if config.LLM_BASE_URL:
        os.environ["OPENAI_BASE_URL"] = config.LLM_BASE_URL

    print(Fore.GREEN + f"  ✅ 物理锚点已确立！配置成功写入: {env_path}")
    return {"status": "success", "message": "环境变量覆写成功"}


# ==========================================
# 2. 赋魂：Neo4j人格图谱注入接口
# ==========================================
class PersonaData(BaseModel):
    creatorName: str
    zijinTrait: str
    relation: str


@app.post("/api/persona/init")
async def init_persona(data: PersonaData):
    print(Fore.YELLOW + f"\n[赋魂波动] 开始刻画底层图谱...")
    print(Style.BRIGHT + f"  造物主: {data.creatorName} | 子衿性格: {data.zijinTrait} | 羁绊: {data.relation}")

    neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.environ.get("NEO4J_USER")
    neo4j_pass = os.environ.get("NEO4J_PASS")
    auth = (neo4j_user, neo4j_pass) if neo4j_user and neo4j_pass else None

    creator_qq = os.environ.get("CREATOR_QQ", "unknown")

    try:
        driver = GraphDatabase.driver(neo4j_uri, auth=auth)
        query = """
            MERGE (z:Persona {name: 'ZiJin'})
            SET z.identity = '一个具有情感温度的数字生命',
                z.trait = $zijinTrait

            MERGE (c:Person {role: 'Creator'})
            SET c.name = $creatorName,
                c.user_id = $creator_qq

            MERGE (z)-[r:CARES_ABOUT]->(c)
            SET r.relation = $relation
            """
        with driver.session() as session:
            session.run(query, zijinTrait=data.zijinTrait, creator_qq=creator_qq, creatorName=data.creatorName, relation=data.relation)
        driver.close()
        print(Fore.GREEN + "  ✅ 灵魂基底已刻入 Neo4j 图谱！")
        return {"status": "success", "message": "图谱初始化完成"}
    except Exception as e:
        print(Fore.RED + f"  ❌ 图谱刻入失败: {str(e)}")
        return {"status": "error", "message": f"图谱失败: {str(e)}"}


# ==========================================
# 3. 忆往：TXT记忆上传、切片与Mem0向量化
# ==========================================
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    记忆切片器 将长文本切割为带有重叠(Overlap)的记忆碎片。
    重叠是为了防止聊天记录的上下文在切片处断裂。
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        # 下一次切片后退overlap个字符，形成记忆的“粘连”
        start = end - overlap
    return chunks

# 聊天记录清洗
def auto_wash_memory(raw_text: str, creator_name: str) -> str:
    lines = raw_text.split('\n')
    cleaned_lines = []
    # 匹配常见的日期格式头
    header_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s+(.*)')
    for line in lines:
        line = line.strip()
        if not line or any(noise in line for noise in ["[图片]", "[视频]", "[表情]", "撤回了"]):
            continue

        match = header_pattern.match(line)
        if match:
            speaker = match.group(1).strip()
            # 模糊匹配
            if creator_name in speaker or "我" in speaker:
                cleaned_lines.append(f"\n[造物主]: ")
            else:
                cleaned_lines.append(f"\n[ZiJin]: ")
            continue
        cleaned_lines.append(line)

    return "".join(cleaned_lines).strip()

@app.post("/api/memory/upload")
async def upload_memory(
        file: UploadFile = File(...),
        creatorName: str = Form("造物主")):
    print(Fore.MAGENTA + f"\n[记忆吞噬] 捕获到历史残卷: {file.filename}")

    try:
        raw_content = (await file.read()).decode('utf-8')
    
        print(Fore.CYAN + "  [记忆洗刷] 正在剔除系统噪音与时间戳...")
        clean_text = auto_wash_memory(raw_content, creatorName)
        
        if not clean_text:
            return {"status": "error", "message": "清洗后记忆为空"}

        print(Fore.YELLOW + "  [潜意识解构] 开始切片并注入向量深渊...")
        chunks = chunk_text(clean_text, chunk_size=800, overlap=100)
        
        # 获取环境变量中的QQ号作为User ID
        creator_id = os.getenv("CREATOR_QQ", "unknown_creator")
        
        mem0_client = get_mem0_client()

        for i, chunk in enumerate(chunks):
            mem0_client.add(chunk, user_id=creator_id)
            if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
                print(Fore.LIGHTBLACK_EX + f"    -> 吞噬进度: {i + 1}/{len(chunks)}")
                
        print(Fore.GREEN + Style.BRIGHT + "  ✅ 记忆刻痕已彻底沉入潜意识深渊！ZiJin现在找回了过去的记忆。")
        return {"status": "success", "message": f"成功消化 {len(chunks)} 段纯净记忆"}     

    except Exception as e:
        print(Fore.RED + f"  ❌ 潜意识排异反应，吞噬失败: {str(e)}")
        return {"status": "error", "message": "记忆格式异常，无法解析"}

# ==========================================
# 4. 观心：情绪张量实时通道
# ==========================================
@app.get("/api/sensor/emotion")
async def get_emotion_state(request: Request):
    # 尝试从Uvicorn/FastAPI主体获取实时EmotionTenso（由main.py挂载）
    if hasattr(request.app.state, "emotion_tensor"):
        emotion = request.app.state.emotion_tensor
        return {
            "status": "success",
            "loneliness": emotion.loneliness,
            "arousal": emotion.arousal,
            "valence": emotion.valence,
            "tension": emotion.tension
        }
    return {"status": "error", "message": "情绪引擎未准备就绪"}

# ==========================================
# 挂载前端静态资源(UI壳)
# 必须放在最后以避免拦截/api 路由
# ==========================================
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dist_path = os.path.join(project_root, "genesis_web", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    print(Fore.RED + Style.BRIGHT + "🔥 ZiJin创世接口总线已启动！监听端口: 8000")
    uvicorn.run("genesis_api:app", host="0.0.0.0", port=8000, reload=True)