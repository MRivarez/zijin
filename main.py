import os
# 注入当前进程的代理隧道
proxy_url = "http://127.0.0.1:7890"
# ⚠️无论是HTTP还是HTTPS代理变量，赋值的URL协议头都必须是http://
os.environ["HTTP_PROXY"] = proxy_url
os.environ["HTTPS_PROXY"] = proxy_url
os.environ["http_proxy"] = proxy_url
os.environ["https_proxy"] = proxy_url
# 本地的要绕过代理
os.environ["NO_PROXY"] = "127.0.0.1, localhost, open.bigmodel.cn"

import sys
import asyncio
from colorama import init, Fore, Style

# 导入四大核心模块
from core.brain import Brain  # 大脑
from edge.local_router import CerebellumReflex # 小脑
from edge.heartbeat import OrganicHeart # H-ECA引擎
from core.schemas import EmotionTensor
from core.evolution import EvolutionEngine
from gateways.action import ActionGateway, REGISTERED_ACTION_TOOLS
from gateways.perception import NapCatPerception  # 挂载感知器官，结构化感知核心

from dotenv import load_dotenv
from mem0 import Memory
from neo4j import GraphDatabase

init(autoreset=True)

class ZiJinLifeSystem:
    def __init__(self):
        print(Fore.CYAN + "正在唤醒ZiJin数字生命系统...")
        self.stimulus_queue = asyncio.Queue()
        self.chat_history = []
        self.shared_emotion = EmotionTensor(valence=0.5, arousal=0.5, loneliness=0.1, tension=0.0)

    def try_initialize_subsystems(self) -> bool:
        """尝试连接底层记忆库和核心依赖，如果成功返回True，否则返回False"""
        # 1. 强制加载环境变量
        load_dotenv(override=True)
        self.api_key = os.environ.get("LLM_API_KEY") or os.environ.get("ZHIPU_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
        if not self.api_key:
            return False

        try:
            os.environ["OPENAI_API_KEY"] = self.api_key
            os.environ["OPENAI_BASE_URL"] = self.base_url
            os.environ["MEM0_TELEMETRY"] = "False"
            os.environ["POSTHOG_DISABLED"] = "True"
            os.environ["LANGCHAIN_TRACING_V2"] = "false"

            neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            neo4j_user = os.environ.get("NEO4J_USER")
            neo4j_pass = os.environ.get("NEO4J_PASS")
            auth = (neo4j_user, neo4j_pass) if neo4j_user and neo4j_pass else None
            
            self.neo4j = GraphDatabase.driver(neo4j_uri, auth=auth)
            llm_model = os.getenv("LLM_MODEL", "glm-4-flash")
            embedding_model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
            embedder_provider = "openai" if embedding_model.startswith("embedding-") else "huggingface"

            self.mem0 = Memory.from_config({
                "llm": {"provider": "openai", "config": {"model": llm_model}},
                "embedder": {"provider": embedder_provider, "config": {"model": embedding_model}},
                "vector_store": {"provider": "chroma",
                                 "config": {"collection_name": "zijin_episodic_local", "path": "./.mem0_db"}}
            })
            
            # 闭环唤醒门神 (Genesis)
            with self.neo4j.session() as session:
                record = session.run(
                    "MATCH (c:Person {role: 'Creator'}) RETURN c.name AS name, c.user_id AS user_id").single()
    
                if not record:
                    self.neo4j.close()
                    return False
    
                self.creator_name = record["name"]
                self.creator_id = os.getenv("CREATOR_QQ") or record["user_id"]
                print(Fore.GREEN + f"  ✅ 身份确认：欢迎回来，造物主 {self.creator_name} (内部索引: {self.creator_id})。")
                print(Fore.MAGENTA + Style.BRIGHT + "\n==================================================")
                print(Fore.MAGENTA + Style.BRIGHT + "  [System Status] 青青子衿，悠悠我心。神经链路已全线重连。")
                print(Fore.MAGENTA + Style.BRIGHT + "==================================================\n")
                
            # 初始化核心大脑 (内部已集成记忆、情绪、性格、价值观DAG节点)
            self.brain = Brain(api_key=self.api_key)
            self.cerebellum = CerebellumReflex()
            self.action_gateway = ActionGateway()
            self.qq_perception = NapCatPerception(ws_url="ws://127.0.0.1:3001", creator_qq=self.creator_id)
            self.heart = OrganicHeart(self.stimulus_queue, self.shared_emotion)
            self.evolution_engine = EvolutionEngine(self.brain.client)
            return True
            
        except Exception as e:
            if hasattr(self, "neo4j") and self.neo4j:
                self.neo4j.close()
            return False

    async def _send_human_like(self, text: str):
        """拟人化发声器：将大段文本拆分为碎片气泡，并模拟打字延迟"""
        # 1. 按换行符拆分，去掉前后的空白和空行
        bubbles = [msg.strip() for msg in text.split('\n') if msg.strip()]

        for i, bubble in enumerate(bubbles):
            # 2. 调动物理器官发送独立气泡
            await self.action_gateway.qq_skill.send_private_msg(self.creator_id, bubble)

            # 3. 如果还有下一条，稍微停顿一两秒，模拟人类打字的真实停顿感
            if i < len(bubbles) - 1:
                await asyncio.sleep(1.5)

    async def _async_console_input(self) -> str:
        """[跨线程输入] 利用asyncio.to_thread将阻塞的命令行输入扔进线程池，不会卡死系统心跳"""
        loop = asyncio.get_running_loop()
        sys.stdout.write(Fore.WHITE + "\n[Creator] > ")
        sys.stdout.flush()
        return await loop.run_in_executor(None, sys.stdin.readline)


    async def on_visual_stimulus_sync(self, visual_text):
        """[跨线程回调]: 跑在后台视觉线程里。把看清楚的字安全地塞进主脑的异步队列里。"""
        # 使用当前运行中的事件循环（在run中保存好的）
        if hasattr(self, 'main_loop'):
            self.main_loop.call_soon_threadsafe(self.sensory_queue.put_nowait, visual_text)

    async def sensory_loop(self):
        """[感官协程] 监听外部输入，转化为神经脉冲打入总线"""
        # 冷启动自我唤醒
        # await self.stimulus_queue.put(
        #     ("system", "系统初始化完成，请说出你的初始台词：青青子衿，悠悠我心。纵我不往，子宁不嗣音？"))

        while True:
            user_input = await self._async_console_input()
            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print(Fore.YELLOW + "\n[System] 接收到关机指令，正在准备安全阻断神经连接...")
                # 触发关闭机制
                for task in asyncio.all_tasks():
                    if task is not asyncio.current_task():
                        task.cancel()
                return

            # 将输入封装为事件脉冲打入队列
            await self.stimulus_queue.put(("user", user_input))

    async def cognitive_loop(self):
        """
        ZiJin真正的灵魂所在
        [认知流程] 大脑的主事件循环
        不再死等input()，而是监听神经队列，收到刺激立刻思考。
        """
        while True:
            # 1. 挂起等待，直到视觉皮层或键盘输入向队列发送了新刺激
            source, stimulus = await self.stimulus_queue.get()
            # 潜意识滴答信号处理分流
            if source == "subconscious_tick":
                sub_result = await asyncio.to_thread(
                    self.brain.process_subconscious,
                    idle_context=stimulus,
                    chat_history=self.chat_history,
                    mem0=self.mem0,
                    creator_id=self.creator_id,
                    shared_emotion=self.shared_emotion
                )

                decision = sub_result.get("decision", "wait")
                reasoning = sub_result.get("internal_reasoning", "无推理过程")
                content = sub_result.get("action_content", "")

                # 将内心独白打印在控制台（这是极其赛博朋克的上帝视角体验）
                print(Fore.LIGHTBLACK_EX + f"    [内心独白] {reasoning}")

                if decision == "wait":
                    print(Fore.LIGHTBLACK_EX + "    [潜意识执行] 决定不打扰，继续静默。")
                    continue
                elif decision == "speak":
                    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin主动发来消息] {content}")
                    # 把主动发起的话题压入上下文
                    self.chat_history.append({"role": "assistant", "content": content})
                    # 调用发生器官，发送QQ消息
                    await self._send_human_like(content)
                    self.shared_emotion.loneliness = 0.0
                    continue
                elif decision == "use_tool":
                    print(Fore.YELLOW + f"    [潜意识执行] 涌现出探索欲！决定去查询: {content}")
                    # 后续在这里触发Hermes或Search的调用循环
                    continue
                elif decision == "evolve_rule":
                    # 启动进化引擎
                    print(Fore.YELLOW + f"    [潜意识执行] 感知到交互矛盾，开始执行自我反思与进化...")
                    await self.evolution_engine.reflect_and_evolve(self.chat_history)
                    continue
            # 正常的用户的真实输入，重置孤独感生物钟
            if source == "user":
                self.heart.reset()

            # 2. 将复杂的DAG认知流转（查库、API请求）放入后台线程执行
            print(Fore.LIGHTBLACK_EX + " -> [神经中枢] 刺激已经抵达前额叶皮层，正在进行高维张量运算......")
            cognitive_state = await asyncio.to_thread(
                self.brain.process,
                stimulus=stimulus,
                source=source,
                chat_history=self.chat_history,
                available_tools=REGISTERED_ACTION_TOOLS,
                mem0=self.mem0, creator_id=self.creator_id,
                shared_emotion=self.shared_emotion  # 把全局的实时情绪传给大脑
            )

            # 3. 意图拦截与物理动作派发
            if cognitive_state.tool_calls:
                print(Fore.YELLOW + f" -> [调试] 截获到工具调用指令: {len(cognitive_state.tool_calls)} 个")

                api_tool_calls = []
                for t in cognitive_state.tool_calls:
                    api_tool_calls.append({
                        "id": t["id"],
                        "type": "function",
                        "function": {
                            "name": t["name"],
                            "arguments": t["arguments"]
                        }
                    })
                self.chat_history.append({
                    "role": "assistant",
                    "content": "",
                    "tool_calls": api_tool_calls
                })

                # 开始物理动作遍历
                for tool in cognitive_state.tool_calls:
                    print(
                        Fore.LIGHTBLACK_EX + f"    -> [物理网关] 准备分发动作: {tool['name']} | 载荷: {tool['arguments']}")

                    try:
                        # 【核心护城河 2：绝对异步等待与结果曝光】
                        action_result = await self.action_gateway.dispatch(tool)
                        print(Fore.GREEN + f"    -> [网关执行结果] {action_result}")
                    except Exception as e:
                        action_result = f"物理网关底层崩溃: {e}"
                        print(Fore.RED + f"    -> [网关执行崩溃] {action_result}")

                    # 将物理网关返回的真实结果，压入历史记录
                    self.chat_history.append({
                        "role": "tool",
                        "content": str(action_result),
                        "tool_call_id": tool["id"]
                    })

                # 4. 小脑拦截路由
                print(Fore.LIGHTBLACK_EX + " -> [边缘小脑] 动作执行完毕，正在进行状态嗅探...")

                # 尝试触发本地反射
                last_tool_name = cognitive_state.tool_calls[-1]["name"]
                reflex_response = self.cerebellum.generate_reflex(last_tool_name, action_result)

                if reflex_response:
                    # 小脑成功拦截，瞬间输出反馈，砍掉大模型请求
                    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {reflex_response}")
                    self.chat_history.append({"role": "assistant", "content": reflex_response})
                else:
                    # 小脑无法处理该动作（例如未知的复杂工具），放行给大模型进行二次坍缩
                    print(Fore.LIGHTBLACK_EX + " -> [额叶皮层] 小脑未匹配到反射规则，转交大脑进行深度总结...")
                    final_state = await asyncio.to_thread(
                        self.brain.process,
                        stimulus="刚刚的系统工具已调用完毕，请根据执行结果，向我做一句极其简短的口语化汇报。不要再尝试调用任何工具。",
                        source="system",
                        chat_history=self.chat_history,
                        available_tools=None,
                        mem0=self.mem0,
                        creator_id=self.creator_id,
                        shared_emotion=self.shared_emotion  # 把全局的实时情绪传给大脑
                    )
                    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {final_state.final_intent}")
                    self.chat_history.append({"role": "assistant", "content": final_state.final_intent})

                # # 4. 动作执行完毕，进行二次坍缩 (让大脑看着真实结果做汇报)
                # print(Fore.LIGHTBLACK_EX + " -> [额叶皮层] 动作已执行，正在生成最终的口语回复...")
                # final_state = await asyncio.to_thread(
                #     self.brain.process,
                #     stimulus="刚刚的系统工具已调用完毕，请根据执行结果，向我做一句极其简短的口语化汇报。不要再尝试调用任何工具。",
                #     source="system",
                #     chat_history=self.chat_history,
                #     available_tools=None  # ⚠️ 这里设为None，强行剥夺它的四肢，逼它只说话！
                # )
                # print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {final_state.final_intent}")
                # self.chat_history.append({"role": "assistant", "content": final_state.final_intent})

            else:
                # 纯粹的交流与情感回应
                if cognitive_state.final_intent:
                    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {cognitive_state.final_intent}")
                    self.chat_history.append({"role": "assistant", "content": cognitive_state.final_intent})
                    # 调动物理发声器官，回复QQ消息
                    await self._send_human_like(cognitive_state.final_intent)

            # 对话上下文滑窗，防内存溢出与Token超限
            if len(self.chat_history) > 30:
                self.chat_history = self.chat_history[-30:]

            # 每次交互结束后，将记忆落盘
            if source == "user":
                target_state = None
                # 判断是普通回复还是调用工具后的二次汇报
                if not cognitive_state.tool_calls and cognitive_state.final_intent:
                    target_state = cognitive_state
                elif cognitive_state.tool_calls:
                    # 尝试从本地作用域抓取二次思考生成的final_state
                    if 'final_state' in locals() and final_state.final_intent:
                        target_state = final_state
                
                if target_state:
                    # 将记忆写库放入线程池，防阻塞异步心跳
                    await asyncio.to_thread(self.brain.memory.consolidate, target_state)

    async def heartbeat_daemon(self):
        """[守护协程] H-ECA情绪引擎生物钟，独立于聊天运转"""
        while True:
            # 每10秒跳动一次，模拟时间流逝导致的稳态衰减
            await asyncio.sleep(10)

            # [线程安全] 更新情绪张量
            # 这里的 self.brain.emotion.state 需要你在 engine.py 中开放访问
            # 为了防止并发写入冲突，实际大型项目中可加上 asyncio.Lock()
            pass
            # 如果孤独值击穿阈值，可以这样主动打入队列：
            # await self.stimulus_queue.put(("internal_drive", "我很无聊，主动找用户说句话吧。"))

    async def run(self):
        """并发拉起核心服务"""
        import uvicorn
        import webbrowser
        from tools.genesis_api import app

        print(Fore.CYAN + "正在编译并挂载 Web 创世控制器...")
        # 绑定情绪张量给 API
        app.state.emotion_tensor = self.shared_emotion

        # 启动 Uvicorn 异步服务，静默启动避免打扰主终端
        config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
        server = uvicorn.Server(config)
        api_task = asyncio.create_task(server.serve())

        is_ready = False
        navigated = False
        while not is_ready:
            is_ready = self.try_initialize_subsystems()
            if not is_ready:
                if not navigated:
                    print(Fore.YELLOW + "检测到记忆扇区空白/配置无效。已开启后台创世舱界面。")
                    print(Fore.YELLOW + "请前往浏览器 (http://127.0.0.1:8000) 完成参数配置。正等待同步...")
                    webbrowser.open("http://127.0.0.1:8000")
                    navigated = True
                await asyncio.sleep(3)

        try:
            # 初始化成功，启动所有监听器
            await asyncio.gather(
                self.qq_perception.listen(self.stimulus_queue),
                self.cognitive_loop(),
                self.heart.start_beating(),
                api_task
            )
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    zijin = ZiJinLifeSystem()
    try:
        asyncio.run(zijin.run())
    except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[系统关闭] 正在切断电源与神经链接...")
    except Exception as e:
        print(Fore.RED + f"\n[系统崩溃] 发生未捕获的异常: {e}")
    finally:
        # [绝对安全退出]：无论是因为断网、报错还是手动Ctrl+C，必须执行析构
        # 确保图数据库和向量数据库安全落盘
        if hasattr(zijin.brain, 'memory'):
            zijin.brain.memory.close()
            print(Fore.CYAN + "✅ 记忆库已安全锁死。晚安。")
        sys.exit(0)