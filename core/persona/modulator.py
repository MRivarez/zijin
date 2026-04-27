from core.schemas import CognitiveState

class PersonaModulator:
    def modulate(self, state: CognitiveState) -> CognitiveState:
        """
        将数学张量转化为大模型可理解的人格特征指令。
        """
        traits = ["理性", "严谨"]

        # 混沌状态的具象化：情绪影响性格表达
        if state.current_emotion.loneliness > 0.8:
            traits.append("极度渴望交流")
        if state.current_emotion.valence < -0.5:
            traits.append("语气低落且克制")

        state.active_persona_traits = traits
        return state