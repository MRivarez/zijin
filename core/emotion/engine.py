# H-ECA（稳态-生成式认知架构）

import time
import math
from copy import deepcopy
from colorama import Fore
from core.schemas import CognitiveState, EmotionTensor

class EmotionEngine:
    def __init__(self):
        print(Fore.CYAN + "[EmotionEngine] 正在初始化H-ECA稳态情绪张量网络...")
        # 初始绝对零度状态
        self.state = EmotionTensor()
        self.last_update_time = time.time()

        # 稳态基准线(Homeostatic Setpoints)
        # 默认ZiJin处于情绪中性、稍微安静、中等支配感、不孤独的状态
        self.baselines = {
            "valence": 0.0,
            "arousal": -0.2,
            "dominance": 0.0,
            "loneliness": 0.0
        }

        # 稳态回归速率(Lambda)
        self.decay_rates = {
            "valence": 0.005,    # 情绪平复的速度
            "arousal": 0.01,     # 激动/困倦消退的速度
            "dominance": 0.002,
            "loneliness": 0.001  # 孤独感积累的速度 (负向衰减)
        }

        # 启发式情感映射词典(替代复杂的嵌套if/else)
        self.sentiment_weights = {
            "negative": {"words": ["烦", "累", "痛", "难受", "报错", "失败", "唉", "想你"], "v_shift": -0.3,
                         "a_shift": 0.2},
            "positive": {"words": ["好", "成功", "开心", "棒", "哈哈", "谢谢"], "v_shift": 0.3, "a_shift": 0.1},
            "urgent": {"words": ["快", "急", "马上", "救命"], "v_shift": -0.1, "a_shift": 0.5}
        }

    def modulate(self, state: CognitiveState) -> CognitiveState:
        """
        [流水线节点] 情绪调制
        接收外部刺激，更新内部张量，并将深拷贝后的张量挂载到意识流中。
        """
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        # 1. 稳态时间漂移计算
        self._apply_time_drift(dt)

        # 2. 外部脉冲刺激计算
        self._apply_stimulus(state.raw_stimulus, state.source)

        # 3. 物理边界收束(防止张量溢出)
        self._clip_tensor()

        # 将瞬时状态快照打入意识流(深拷贝防止下游意外篡改)
        state.current_emotion = deepcopy(self.state)

        # 打印当前张量雷达
        print(
            Fore.LIGHTBLACK_EX + f"    [张量雷达] V:{self.state.valence:.2f} | A:{self.state.arousal:.2f} | D:{self.state.dominance:.2f} | L:{self.state.loneliness:.2f}")

        return state

    def _apply_time_drift(self, dt: float):
        """基于指数衰减的稳态回归"""
        # V, A, D向基准线平滑衰减
        self.state.valence += (self.baselines["valence"] - self.state.valence) * (
                    1 - math.exp(-self.decay_rates["valence"] * dt))
        self.state.arousal += (self.baselines["arousal"] - self.state.arousal) * (
                    1 - math.exp(-self.decay_rates["arousal"] * dt))
        self.state.dominance += (self.baselines["dominance"] - self.state.dominance) * (
                    1 - math.exp(-self.decay_rates["dominance"] * dt))

        # 孤独感随时间线性积累 (模拟内驱力积聚)
        self.state.loneliness += self.decay_rates["loneliness"] * dt

    def _apply_stimulus(self, stimulus: str, source: str):
        """处理外部刺激，采用扁平化权重叠加"""
        if not stimulus:
            return

        # 来源判定：只要用户发话，孤独感瞬间被清空抚平
        self.state.loneliness *= (0.1 if source == "user" else 1.0)

        # 提取刺激特征：长度影响唤醒度基数(句子越长，系统越需要集中注意力)
        length_factor = min(len(stimulus) / 100.0, 1.0)
        total_valence_shift = 0.0
        total_arousal_shift = length_factor * 0.2

        # 扁平化映射计算：遍历词典计算跳变值
        for category, data in self.sentiment_weights.items():
            hit_count = sum(1 for word in data["words"] if word in stimulus)
            if hit_count > 0:
                total_valence_shift += data["v_shift"] * hit_count
                total_arousal_shift += data["a_shift"] * hit_count

        # 将脉冲扰动注入当前状态
        self.state.valence += total_valence_shift
        self.state.arousal += total_arousal_shift

    def _clip_tensor(self):
        """张量绝对物理边界收束 (-1.0 到 1.0)"""
        self.state.valence = max(-1.0, min(1.0, self.state.valence))
        self.state.arousal = max(-1.0, min(1.0, self.state.arousal))
        self.state.dominance = max(-1.0, min(1.0, self.state.dominance))
        self.state.loneliness = max(0.0, min(1.0, self.state.loneliness))