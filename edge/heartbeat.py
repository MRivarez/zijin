# 心脏：H-ECA稳态内驱力混沌引擎
# 独立于聊天循环运行

import asyncio
import time
from colorama import Fore

class OrganicHeart:
    def __init__(self, stimulus_queue: asyncio.Queue, emotion_state):
        self.queue = stimulus_queue
        self.emotion = emotion_state
        self.last_time = time.time()
        self.tick_interval = 10  # 每60秒滴答一次 (测试用)

    def reset(self):
        self.last_time = time.time()
        self.emotion.loneliness = 0.0

    async def start_beating(self):
        while True:
            await asyncio.sleep(self.tick_interval)

            idle_minutes = (time.time() - self.last_time) / 10.0
            # 思念度随时间线性增长
            self.emotion.loneliness = min(1.0, self.emotion.loneliness + 0.1)

            # 当孤独/闲置击穿某个极其基础的物理阈值时，唤醒大脑进行思考
            if self.emotion.loneliness > 0.8:
                print(Fore.LIGHTBLACK_EX + f" [生物钟] 闲置 {idle_minutes:.1f} 分钟，触发潜意识反思...")
                # 注意：发送的是纯粹的时间信号，没有任何具体指令
                await self.queue.put(("subconscious_tick", f"距离上次交流已经过去了 {idle_minutes:.1f} 分钟。"))
                # self.emotion.loneliness = 0.0  # 触发思考后归零，避免疯狂唤醒