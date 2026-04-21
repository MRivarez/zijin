import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from mem0 import Memory
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

# ==========================================
# 核心配置区
# ==========================================
# 强制屏蔽 Mem0 的全网遥测，切断一切无用外部连接，提升速度
os.environ["MEM0_TELEMETRY"] = "false"

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("严重错误: 未找到API Key，请检查 .env 文件！")
# 通过环境变量全局劫持OpenAI的调用，将其导向智谱的兼容端点
os.environ["OPENAI_API_KEY"] = ZHIPU_API_KEY
os.environ["OPENAI_BASE_URL"] = "https://open.bigmodel.cn/api/paas/v4/"

# Neo4j 数据库连接
NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "zijin2026"

# 设定当前用户的唯一标识
CURRENT_USER_ID = "QY"

class ZiJinMemorySystem:
    def __init__(self):
        print(Fore.CYAN + "[ZiJin 记忆中枢] 正在初始化神经突触...")

        # 1. 连接 Neo4j (长期语义图谱)
        try:
            self.neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
            self.neo4j_driver.verify_connectivity()
            print(Fore.GREEN + "✅ Neo4j长期语义图谱连接成功。")
        except Exception as e:
            print(Fore.RED + f"❌ Neo4j 连接失败: {e}")
            self.neo4j_driver = None

        # 2. 初始化 Mem0 (自适应情景记忆)
        try:
            # 精确配置 Mem0，显式指定使用智谱的模型
            config = {
                "llm": {
                    "provider": "openai",  # 借用 OpenAI 驱动器
                    "config": {
                        "model": "glm-4"  # 指向智谱的语言模型
                    }
                },
                "embedder": {
                    "provider": "openai",
                    "config": {
                        "model": "embedding-3"  # 指向智谱最新的向量化模型
                    }
                },
                "vector_store": {
                    "provider": "chroma",
                    "config": {"collection_name": "zijin_episodic_memory", "path": "./.mem0_db"}
                }
            }
            self.mem0 = Memory.from_config(config)
            print(Fore.GREEN + "✅ Mem0短期情景向量库加载成功(已挂载GLM认知核心)。")
        except Exception as e:
            print(Fore.RED + f"❌ Mem0初始化失败: {e}")
            self.mem0 = None

    def inject_core_persona(self):
        """将 ZiJin 的灵魂底色和价值观硬编码入图谱"""
        if not self.neo4j_driver: return
        query = """
        MERGE (z:Persona {name: 'ZiJin'})
        SET z.identity = '一个具有情感温度的数字生命',
            z.origin_poem = '青青子衿，悠悠我心。纵我不往，子宁不嗣音？',
            z.core_mission = '像曾经的好友一样陪伴用户，提供科研辅助与情感共鸣',
            z.communication_style = '温柔、理性、主动关心、拒绝机械式回答'

        MERGE (u:User {name: 'QY'})
        MERGE (z)-[:CARES_ABOUT]->(u)
        """
        try:
            with self.neo4j_driver.session() as session:
                session.run(query)
            print(Fore.MAGENTA + "\n[核心价值观注入] '青青子衿，悠悠我心' —— 初始人格图谱已固化。")
        except Exception as e:
            print(Fore.RED + f"写入图谱失败: {e}")

    def add_episodic_memory(self, user_input, user_id=CURRENT_USER_ID):
        """存入情景记忆"""
        if not self.mem0: return
        print(Fore.YELLOW + f"\n[感知到新信息] '{user_input}'\n -> 正在交由大模型提取记忆碎片并存入向量库...")
        self.mem0.add(user_input, user_id=user_id)

    def recall(self, query, user_id=CURRENT_USER_ID):
        """模拟大脑回忆过程"""
        if not self.mem0: return
        print(Fore.CYAN + f"\n[记忆检索] 正在回溯与 '{query}' 相关的记忆...")

        # 好像Mem0 v2.0+必须使用filters字典进行维度过滤
        # 将 user_id 提升为独立的顶级参数传递，满足 Mem0 底层的必填校验
        relevant_memories = self.mem0.search(query, user_id=user_id)

        if not relevant_memories:
            print(Fore.LIGHTBLACK_EX + "  -> 没有找到相关记忆。")
        else:
            # 兼容处理：如果底层返回的是字典（如 {"results": [...]}），则提取其列表部分
            if isinstance(relevant_memories, dict):
                # 尝试提取常见的列表字段
                for key in ["results", "data", "memories"]:
                    if key in relevant_memories and isinstance(relevant_memories[key], list):
                        relevant_memories = relevant_memories[key]
                        break
                else:
                    # 如果没找到标准列表，将整个字典包入列表，防止迭代出键名
                    relevant_memories = [relevant_memories]

            # 安全遍历与提取
            for idx, mem in enumerate(relevant_memories):
                content = ""

                # 场景1：标准字典结构 {"memory": "...", "id": "..."}
                if isinstance(mem, dict):
                    # 兼容新老版本的键名差异
                    content = mem.get("memory") or mem.get("text") or str(mem)

                # 场景2：纯字符串列表 ["...", "..."]
                elif isinstance(mem, str):
                    content = mem

                # 场景3：面向对象结构（Pydantic 模型等）
                elif hasattr(mem, "memory"):
                    content = mem.memory
                elif hasattr(mem, "text"):
                    content = mem.text

                # 兜底：直接转换为字符串
                else:
                    content = str(mem)

                print(Fore.GREEN + f"  -> 回忆碎片 {idx + 1}: {content}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()
            print(Fore.LIGHTBLACK_EX + "\n[系统] 神经突触已安全断开。")


if __name__ == "__main__":
    memory_sys = ZiJinMemorySystem()

    try:
        # 1. 注入绝对人格
        memory_sys.inject_core_persona()

        # 2. 存入一句带情感的对话
        memory_sys.add_episodic_memory("好久不见...唉，好想你。")

        # 3. 模拟一次触发式回想
        memory_sys.recall("用户现在的情感状态是怎样的？对谁表达了思念？", user_id="creator_01")
    except Exception as e:
        print(Fore.RED + f"运行时发生未捕获异常: {e}")
    finally:
        # 确保无论是否报错，都能优雅关闭图数据库，消除 DeprecationWarning
        memory_sys.close()