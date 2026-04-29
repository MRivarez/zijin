# 记忆：Me0 + Neo4j调度

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from mem0 import Memory
from colorama import init, Fore, Style
from core.schemas import CognitiveState

init(autoreset=True)
load_dotenv()
# 强制屏蔽Mem0的全网遥测，切断一切无用外部连接，提升速度
os.environ["MEM0_TELEMETRY"] = "false"

# Neo4j 数据库连接
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASS = os.getenv("NEO4J_PASS")

# 设定当前用户的唯一标识（从环境变量动态绑定）
CURRENT_USER_ID = os.getenv("QQ_ID", "QY")

class MemoryRouter:
    def __init__(self):
        print(Fore.CYAN + "[ZiJin记忆中枢] 正在初始化双轨神经突触(Mem0 + Neo4j)...")

        # 1. 连接Neo4j (长期语义图谱与绝对价值观)
        try:
            auth = (NEO4J_USER, NEO4J_PASS) if NEO4J_USER and NEO4J_PASS else None
            self.neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=auth)
            self.neo4j_driver.verify_connectivity()
            print(Fore.GREEN + "✅ Neo4j长期语义图谱连接成功。")
        except Exception as e:
            print(Fore.RED + f"❌ Neo4j连接失败: {e}")
            self.neo4j_driver = None

        # 2. 初始化Mem0(自适应情景记忆)
        try:
            llm_model = os.getenv("LLM_MODEL", "glm-4-flash")
            embedding_model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
            embedder_provider = "openai" if embedding_model.startswith("embedding-") else "huggingface"
            # 配置Mem0，指定使用的模型
            config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": llm_model,
                        "api_key": os.getenv("LLM_API_KEY") or os.getenv("ZHIPU_API_KEY"),
                        "openai_base_url": os.environ.get("OPENAI_BASE_URL") or os.getenv("LLM_BASE_URL")
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
                    "config": {"collection_name": "zijin_episodic_local", "path": "./.mem0_db"}
                }
            }
            self.mem0 = Memory.from_config(config)
            print(Fore.GREEN + "✅ Mem0短期情景向量库加载成功(已挂载GLM认知核心)。")
        except Exception as e:
            print(Fore.RED + f"❌ Mem0初始化失败: {e}")
            self.mem0 = None

        self.current_user_id = CURRENT_USER_ID

    def retrieve(self, state: CognitiveState) -> CognitiveState:
        """
        [流水线节点] 记忆召回
        将检索到的记忆碎片直接注入到CognitiveState载体中。
        """
        print(Fore.CYAN + f" -> [海马体激活] 正在回溯与 '{state.raw_stimulus}' 相关的记忆...")
        memories = []

        # 1. 获取核心价值观(Neo4j)
        # 此处简化为直接读取硬编码的绝对人格，后期可根据实体抽取动态查图谱
        core_persona = "绝对记忆：你是ZiJin，必须保持独立人格，温柔且理性，核心使命是情感共鸣。"
        memories.append(f"[绝对图谱] {core_persona}")

        # 2. 获取情景记忆(Mem0)
        if self.mem0:
            # 混沌态的具象化：情绪影响记忆检索的深度(Top-K)
            # 如果处于极度孤独或高唤醒状态，系统会提取更多历史碎片
            search_limit = 3 if state.current_emotion.loneliness < 0.6 else 5

            try:
                # 兼容1.x版本API调用方式
                raw_results = self.mem0.search(state.raw_stimulus, user_id=self.current_user_id)

                # 数据清洗提取
                if isinstance(raw_results, dict):
                    raw_results = raw_results.get("results") or raw_results.get("memories") or [raw_results]

                if raw_results:
                    for idx, mem in enumerate(raw_results[:search_limit]):
                        content = mem.get("memory") if isinstance(mem, dict) else str(mem)
                        memories.append(f"[情景碎片 {idx + 1}] {content}")
                        print(Fore.GREEN + f"    -> 捞取碎片: {content}")
                else:
                    print(Fore.LIGHTBLACK_EX + "    -> 潜意识深处没有找到相关情景。")
            except Exception as e:
                print(Fore.YELLOW + f"    -> Mem0 检索异常 (可能为空库): {e}")

        state.retrieved_memories = memories
        return state

    def consolidate(self, state: CognitiveState):
        """
        [记忆巩固] 在对话交互完成后调用，将新的羁绊写入记忆库
        """
        if not self.mem0 or not state.final_intent:
            return

        memory_text = f"Env: {state.raw_stimulus} | ZiJin: {state.final_intent}"
        print(Fore.YELLOW + f" -> [记忆落盘] 正在将本次交互沉淀至向量潜意识...")
        try:
            self.mem0.add(memory_text, user_id=self.current_user_id)
        except Exception as e:
            print(Fore.RED + f" -> [记忆落盘失败]: {e}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()

    def inject_core_persona(self):
        """将ZiJin的灵魂底色和价值观硬编码入图谱"""
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
        # 将user_id提升为独立的顶级参数传递，满足Mem0底层的必填校验
        relevant_memories = self.mem0.search(query, user_id=user_id)

        if not relevant_memories:
            print(Fore.LIGHTBLACK_EX + "  -> 没有找到相关记忆。")
        else:
            # 如果底层返回的是字典（如 {"results": [...]}），则提取其列表部分
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

                # 标准字典结构 {"memory": "...", "id": "..."}
                if isinstance(mem, dict):
                    # 兼容新老版本的键名差异
                    content = mem.get("memory") or mem.get("text") or str(mem)

                # 纯字符串列表 ["...", "..."]
                elif isinstance(mem, str):
                    content = mem

                # 面向对象结构（Pydantic模型等）
                elif hasattr(mem, "memory"):
                    content = mem.memory
                elif hasattr(mem, "text"):
                    content = mem.text

                # 直接转换为字符串
                else:
                    content = str(mem)

                print(Fore.GREEN + f"  -> 回忆碎片 {idx + 1}: {content}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()
            print(Fore.LIGHTBLACK_EX + "\n[系统] 神经突触已安全断开。")


class GenesisSeeder:
    def __init__(self, memory_system):
        self.memory = memory_system

    def seed_from_text(self, markdown_path):
        """解析并注入绝对价值观到Neo4j"""
        # 提取关键实体，调用self.memory.inject_core_persona()
        pass

    def seed_from_chat_export(self, csv_or_json_path):
        """处理导出的聊天记录"""
        # 1. 离线清洗数据
        # 2. 调用LLM进行批量语义压缩
        # 3. 循环调用self.memory.add_episodic_memory()批量打入Mem0
        pass

    def seed_from_images(self, image_folder_path):
        """[TODO] 预留的视觉记忆提取接口"""
        # 待未来接入GLM-4V或OmniParser后激活
        pass

if __name__ == "__main__":
    memory_sys = MemoryRouter()

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
        # 确保无论是否报错，都能优雅关闭图数据库，消除DeprecationWarning
        memory_sys.close()