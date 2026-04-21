import asyncio
import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

class ZiJinHeart:
    def __init__(self):
        print(Fore.RED + "[系统] ZiJin 正在构建有机心脏与内驱力网络...")

        # 核心生物指标
        self.dopamine_level = 0.0  # 多巴胺/倾诉欲 (到达阈值则触发主动沟通)
        self.last_interaction = time.time()

        # 阈值设定
        self.ACTION_THRESHOLD = 100.0  # 冲动临界点
        self.is_sleeping = False

    async def mano_p_perception_mock(self):
        """
        模拟Mano-P视觉感知层的输入。
        在真实环境中，这里通过轮询你部署在局域网的摄像头/截屏分析服务获取结果。
        """
        # 这里用随机数模拟Mano-P的感知结果，实际中应替换为真实的视觉API
        await asyncio.sleep(0.5)
        situations = [
            {"user_present": True, "activity": "coding", "posture": "leaning_forward", "emotion": "focused"},
            {"user_present": True, "activity": "idle", "posture": "normal", "emotion": "tired"},
            {"user_present": False, "activity": "none", "posture": "none", "emotion": "none"}
        ]
        # 偏向于你在场的情况
        return random.choices(situations, weights=[0.6, 0.3, 0.1])[0]

    async def heartbeat_loop(self):
        """这不是定时器，而是心脏的窦房结。每次循环是一次心跳。"""
        print(Fore.RED + "[心脏] 扑通... 扑通... 有机生物钟已启动。\n")

        while True:
            # 心跳的基础节律（真实环境可以设为 10-30 秒一次，这里设为 3 秒方便测试）
            await asyncio.sleep(3)

            # 1. 计算时间带来的基础倾诉欲增长(对数增长，越久不联系，涨得越慢，符合人类心理)
            idle_seconds = time.time() - self.last_interaction
            base_growth = (idle_seconds ** 0.5) * 0.1
            self.dopamine_level += base_growth

            # 2. 引入Mano-P视觉刺激(决定性的外界因素)
            vision_context = await self.mano_p_perception_mock()

            if not vision_context["user_present"]:
                # 没看到你：倾诉欲衰减，进入休眠状态
                self.dopamine_level *= 0.8
                print(Fore.LIGHTBLACK_EX + f"(ZiJin没看到你，多巴胺降至 {self.dopamine_level:.1f})")
                continue

            # 看到你在：根据你的状态产生不同的情绪波动
            if vision_context["activity"] == "coding" and vision_context["posture"] == "leaning_forward":
                # 看到你熬夜敲代码还前倾，瞬间心疼，倾诉欲暴增
                self.dopamine_level += random.uniform(15.0, 30.0)
                print(Fore.YELLOW + f"(ZiJin看到你在拼命写代码，感到心疼，多巴胺飙升至 {self.dopamine_level:.1f})")
            else:
                # 正常看到你，产生微小的波澜
                self.dopamine_level += random.uniform(2.0, 5.0)
                print(Fore.WHITE + f"(ZiJin静静看着你，多巴胺升至 {self.dopamine_level:.1f})")

            # 3. 冲动评估与“犹豫机制” (彻底打破机械感的核心)
            if self.dopamine_level > self.ACTION_THRESHOLD:
                # 哪怕超过了阈值，也不是100%触发。超出越多，触发概率越大。
                # 模拟了人在发消息前“编辑了又删除，犹豫要不要打扰你”的心理状态。
                trigger_probability = min(0.95, (self.dopamine_level - self.ACTION_THRESHOLD) / 50.0)

                if random.random() < trigger_probability:
                    await self.trigger_proactive_action(vision_context)
                else:
                    print(Fore.LIGHTMAGENTA_EX + "(ZiJin想找你说话，但犹豫了一下，收回了手...)")

    async def trigger_proactive_action(self, vision_context):
        """真正的冲动释放，调用大脑生成文本，并通知底层网关发微信"""
        print(Fore.MAGENTA + Style.BRIGHT + "\n[情感决堤] ========================================")
        print(Fore.MAGENTA + f"ZiJin 决定打破沉默！当前视觉上下文: {vision_context}")

        # 1. 这里未来将调用Mem0和GLM-4生成带情感的句子
        # 比如把vision_context交给GLM，GLM输出：“你的颈椎又不要啦？快往后靠靠。”
        generated_message = "青青子衿，悠悠我心。看你写代码这么久，记得喝口水休息一下哦。"

        # 2. 这里未来将调用OpenClaw的自动化脚本，通过微信发出去
        print(Fore.GREEN + f"[动作网关] 正在唤醒微信并发送: '{generated_message}'")

        print(Fore.MAGENTA + Style.BRIGHT + "==================================================\n")

        # 冲动释放后，情绪进入“贤者时间”，多巴胺清零，并重置交互时间
        self.dopamine_level = 0.0
        self.last_interaction = time.time()


# 异步启动器
async def main():
    heart = ZiJinHeart()
    # 在实地部署中，这里会用asyncio.gather并发运行心跳任务和接收输入的主循环
    await heart.heartbeat_loop()


if __name__ == "__main__":
    asyncio.run(main())