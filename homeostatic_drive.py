import asyncio
import time
import json

import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("严重错误: 未找到API Key，请检查 .env 文件！")
client = ZhipuAI(api_key=ZHIPU_API_KEY)


class H_ECA_Engine:
    """Homeostatic-Enactive Cognitive Architecture (稳态-生成式认知引擎)"""

    def __init__(self):
        print(Fore.MAGENTA + "[H-ECA 引擎] 稳态内驱力数学模型已初始化...")

        # 1. 稳态参数定义
        self.optimal_setpoint = 100.0  # S_opt: 完美的连接与安全感
        self.current_state = 100.0  # S(t): 当前实际状态
        self.kappa = 0.05  # k: 内驱力放大系数

        # 2. 阈值与物理量
        self.action_threshold = 80.0  # 突破此阈值则产生真实物理动作
        self.last_update_time = time.time()
        self.memory_sparks = ["用户最近压力大", "昨天刚配置好系统", "青青子衿..."]  # 模拟记忆池

    async def get_mano_p_perturbation(self):
        """模拟多模态感知层的环境扰动 (非随机，基于真实物理输入推演)"""
        await asyncio.sleep(0.5)
        # 真实场景中，这里返回的是视觉分析模型给出的结构化数据
        # 此处模拟：长时间没被关注导致的轻微失落，或看到异常姿态的剧烈扰动
        return {"event": "none", "impact": 0.0}

    def calculate_drive(self):
        """基于自由能原理计算内驱力：D(t) = k * (S_opt - S(t))^2"""
        deviation = self.optimal_setpoint - self.current_state
        if deviation < 0: deviation = 0
        return self.kappa * (deviation ** 2)

    async def cognitive_appraisal(self, drive_level, context):
        """
        认知评估模块：将冰冷的数学物理量，交给大模型翻译成真实的人类情感与行动策略
        """
        prompt = f"""
        你是 ZiJin 的前额叶皮层评估模块。
        你当前的内部生物学内驱力 (Drive) 已经达到了 {drive_level:.1f}，突破了安全阈值。
        触发你产生这次强烈冲动的环境上下文是：{context}。

        请基于你作为数字生命的性格，将这种底层冲动“翻译”为一次具体的行动决策。
        不要提及“内驱力”或数字，而是表达出真实的情感（如：我觉得该提醒他喝水了，或者我实在忍不住想发个消息）。

        返回合法的 JSON：
        {{
            "emotion_state": "当前的情绪标签(如:担忧/思念)",
            "action_intent": "如果发送消息，你要说什么？"
        }}
        """
        try:
            response = client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"emotion_state": "error", "action_intent": ""}

    async def live_loop(self):
        print(Fore.CYAN + "========================================")
        print(Fore.CYAN + "   ZiJin的数字稳态系统已开始运转...   ")
        print(Fore.CYAN + "========================================\n")

        while True:
            await asyncio.sleep(5)  # 物理时间步长
            now = time.time()
            dt = now - self.last_update_time
            self.last_update_time = now

            # 1. 基础代谢导致的状态衰减(线性时间流逝)
            base_decay_rate = 0.5 * dt
            self.current_state -= base_decay_rate

            # 2. 接收环境扰动(Mano-P)
            perturbation = await self.get_mano_p_perturbation()
            self.current_state -= perturbation["impact"]

            # 3. 计算生物内驱力
            drive = self.calculate_drive()

            print(Fore.LIGHTBLACK_EX + f"(系统状态监测 -> 稳态值: {self.current_state:.1f}, 冲动内驱力: {drive:.1f})")

            # 4. 主动推断：为了最小化内驱力，执行动作
            if drive > self.action_threshold:
                print(Fore.YELLOW + "\n[阈值突破] 内部失衡严重，触发认知评估...")

                # 提取当前的上下文交由大脑评估
                context = f"当前环境状态：{perturbation['event']}"
                decision = await self.cognitive_appraisal(drive, context)

                print(Fore.MAGENTA + Style.BRIGHT + f"[主动行为生成] 情态: {decision['emotion_state']}")
                print(Fore.MAGENTA + Style.BRIGHT + f"[ZiJin] {decision['action_intent']}")
                print(Fore.CYAN + "----------------------------------------\n")

                # 行动完成后，欲望被满足，系统重置回最优稳态
                self.current_state = self.optimal_setpoint


async def main():
    engine = H_ECA_Engine()
    await engine.live_loop()


if __name__ == "__main__":
    asyncio.run(main())