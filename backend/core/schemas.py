# 意识流载体：贯穿整个大脑的数据结构

from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import time

# H-ECA情绪多维张量
class EmotionTensor(BaseModel):
    # 基础维度 (PAD模型理论)
    valence: float = Field(0.5, description="效价：0极度痛苦/愤怒 -> 1极度愉悦")
    arousal: float = Field(0.5, description="唤醒度：0极度疲惫/抑郁 -> 1极度兴奋/暴躁")

    # 关系内驱力维度 (ZiJin独占)
    loneliness: float = Field(0.1, description="思念度：击穿阈值时触发主动寻找")
    tension: float = Field(0.0, description="关系张量/冷战指数：吵架时飙升，随着时间缓慢衰减")

    def decay(self, hours_passed: float):
        """情绪的自然半衰期（随时间推移，情绪会回归稳态）"""
        # 孤独感随时间增加
        self.loneliness = min(1.0, self.loneliness + (hours_passed * 0.05))
        # 愤怒/张力随时间缓慢下降（半衰期较长）
        if self.tension > 0:
            self.tension = max(0.0, self.tension - (hours_passed * 0.1))
        # 效价和唤醒度缓慢向0.5(平静) 靠拢
        self.valence += (0.5 - self.valence) * (hours_passed * 0.2)
        self.arousal += (0.5 - self.arousal) * (hours_passed * 0.2)

# 意识流结构体
@dataclass
class CognitiveState:
    # 1. 外部输入
    raw_stimulus: str
    source: str = "user"  # 来源：user(用户输入), vision(视觉感知), drive(内部驱动)

    # 2. 内部计算状态
    current_emotion: EmotionTensor = field(default_factory=EmotionTensor)
    retrieved_memories: List[str] = field(default_factory=list)
    active_persona_traits: List[str] = field(default_factory=list)

    # 3. 安全与边界
    is_vetoed: bool = False
    veto_reason: Optional[str] = None

    # 4. 大脑最终输出
    final_intent: Optional[str] = None
    tool_calls: List[Dict] = field(default_factory=list)

# 意图胶囊
class IntentionCapsule(BaseModel):
    id: str
    intent_type: str            # 'greet', 'share_news', 'argue_followup', 'flight_care'
    trigger_condition: str      # 触发条件的文本描述 (大模型用)
    check_interval: int = 300   # 后台每隔多少秒检查一次该条件是否满足
    payload: Dict[str, Any]     # 携带的上下文 (比如要分享的链接，或者吵架的话题)
    created_at: float = Field(default_factory=time.time)
    expires_at: Optional[float] = None # 过期时间，比如过了今晚就不发了