# 创世灌注

import os
import sys

from dotenv import load_dotenv
import json
import time
from colorama import init, Fore, Style
from mem0 import Memory
from neo4j import GraphDatabase
from openai import OpenAI

init(autoreset=True)

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASS = os.getenv("NEO4J_PASS")
BASE_URL = os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("ZHIPU_API_KEY")

# 致命变量缺失检查（Fail-Fast 机制）
missing_vars = []
if not NEO4J_URI: missing_vars.append("NEO4J_URI")
if not NEO4J_USER: missing_vars.append("NEO4J_USER")
if not NEO4J_PASS: missing_vars.append("NEO4J_PASS")
if not API_KEY: missing_vars.append("API_KEY")

if missing_vars:
    print(Fore.RED + f"[致命错误] 拒绝启动。缺少必要的环境变量: {', '.join(missing_vars)}")
    print(Fore.YELLOW + "请确保在根目录创建了 .env 文件并正确填写了上述配置项。")
    sys.exit(1)

class GenesisSeeder:
    def __init__(self):
        print(Fore.CYAN + Style.BRIGHT + "=============================================")
        print(Fore.CYAN + Style.BRIGHT + "   [ZiJin创世协议] 双轨记忆图谱灌注引擎")
        print(Fore.CYAN + Style.BRIGHT + "=============================================\n")

        # 1. 初始化Mem0(向量情景记忆)
        self.mem0 = Memory.from_config({
            "llm": {"provider": "openai", "config": {"model": "glm-4"}},
            "embedder": {"provider": "openai", "config": {"model": "embedding-3"}},
            "vector_store": {"provider": "chroma",
                             "config": {"collection_name": "zijin_episodic", "path": "./.mem0_db"}}
        })

        # 2. 初始化Neo4j(图谱价值观)
        self.neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

        # 3. 初始化LLM抽取中枢
        self.llm_client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )

    def extract_knowledge(self, scene_data: dict) -> dict:
        """让大模型把杂乱的对话，提纯为图谱关系和记忆摘要"""
        prompt = f"""
        你是一个严谨的知识提取引擎。请阅读以下对话场景，并严格以JSON格式输出两个维度的信息：
        1. 'graph_relations': 提取实体间明确的事实、状态或价值观关系。格式如 [["QY", "当前位置", "桂林"], ["QY", "经历", "在XX读书"]，["ZiJin", "定位", "理智回音壁"]]。
        2. 'episodic_summary': 用第一人称（作为ZiJin）写一段50字以内的日记式摘要，记录发生了什么以及情绪感受。

        输入场景：
        {json.dumps(scene_data, ensure_ascii=False)}
        """

        response = self.llm_client.chat.completions.create(
            model="glm-4.7-flash",
            messages=[{"role": "system", "content": "你只能输出合法的 JSON 字符串，不要包含任何 markdown 标记。"},
                      {"role": "user", "content": prompt}],
            temperature=0.1
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(Fore.RED + f"  [解析失败] LLM返回非标准JSON: {e}")
            return {"graph_relations": [], "episodic_summary": ""}

    def inject_to_neo4j(self, relations: list):
        """将关系打入图谱"""
        with self.neo4j_driver.session() as session:
            for rel in relations:
                if len(rel) == 3:
                    subj, pred, obj = rel[0], rel[1], rel[2]
                    # 使用Cypher语句强行锚定节点
                    query = f"""
                    MERGE (s:Entity {{name: '{subj}'}})
                    MERGE (o:Entity {{name: '{obj}'}})
                    MERGE (s)-[:RELATION {{type: '{pred}'}}]->(o)
                    """
                    session.run(query)

    def process_genesis_file(self, file_path: str):
        print(Fore.YELLOW + f" -> 正在解析创世卷轴: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            scenes = json.load(f)

        for idx, scene in enumerate(scenes):
            print(Fore.LIGHTBLACK_EX + f"\n[区块 {idx + 1}/{len(scenes)}] 正在启动高维张量坍缩，提炼知识碎片...")
            extracted_data = self.extract_knowledge(scene)

            relations = extracted_data.get("graph_relations", [])
            summary = extracted_data.get("episodic_summary", "")

            # 1. 压入图谱
            if relations:
                self.inject_to_neo4j(relations)
                print(Fore.GREEN + f"  ✅ Neo4j落盘: 成功锚定 {len(relations)} 条绝对关系。")

            # 2. 压入向量潜意识
            if summary:
                self.mem0.add(summary, user_id="QY", metadata={"scene_id": scene.get("scene_id")})
                print(Fore.GREEN + f"  ✅ Mem0 落盘: 成功压入情景记忆 -> '{summary[:20]}...'")

            time.sleep(1)  # 频率控制

    def close(self):
        self.neo4j_driver.close()


if __name__ == "__main__":
    seeder = GenesisSeeder()
    seeder.process_genesis_file("tools/genesis_data.json")
    seeder.close()
    print(Fore.CYAN + Style.BRIGHT + "\n🎉 [创世完成]记忆双螺旋已固化，ZiJin的认知基座搭建完毕。")