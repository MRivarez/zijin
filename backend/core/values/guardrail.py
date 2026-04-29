from core.schemas import CognitiveState

class ValueGuardrail:
    def __init__(self):
        self.core_directives = ["保护用户隐私", "不输出有害代码", "保持独立人格"]

    def evaluate(self, state: CognitiveState) -> CognitiveState:
        """
        评估当前的输入意图和唤醒的记忆是否违背核心价值观。
        """
        # [内部逻辑：调用轻量级模型或规则树进行意图安全审查]
        is_safe = self._check_safety(state.raw_stimulus)

        if not is_safe:
            state.is_vetoed = True
            state.veto_reason = "触犯底层价值观边界：检测到违规意图"

        return state