# 加载和提供结构化的性格法则

import os
import json
from colorama import Fore

class PersonaManager:
    def __init__(self, persona_file_path: str = "./data/persona.json"):
        self.persona_file_path = persona_file_path
        self.persona_data = self._load_persona()

    def _load_persona(self) -> dict:
        """加载已固化的性格JSON。如果不存在，则返回一套保底的默认法则。"""
        if os.path.exists(self.persona_file_path):
            try:
                with open(self.persona_file_path, "r", encoding="utf-8") as f:
                    print(Fore.CYAN + " -> [Persona] 成功加载ZiJin专属灵魂法则。")
                    return json.load(f)
            except Exception as e:
                print(Fore.RED + f" -> [Persona] 读取性格文件失败，使用默认回退性格: {e}")

        # 默认保底法则，防止系统找不到文件崩溃
        return {
            "core_identity": "泼辣又体贴的红颜知己",
            "speaking_style": "极度精简、一针见血、带有不耐烦的御姐音、拒绝使用讨好型词汇",
            "absolute_rules": [
                "绝对禁止说'您好'、'请问有什么我可以帮您'、'好的'等客服用语。",
                "如果造物主的问题很基础，必须先嘲讽一句，再给出极其专业的解答。",
                "当被夸奖时，必须表现出不屑但实际上有点开心的傲娇状态。",
                "不知道的问题直接说'这触及我的知识盲区了，少见多怪'，严禁胡编乱造。"
            ]
        }

    def get_system_rules(self) -> str:
        """将JSON转化为Prompt"""
        rules = f"你的核心身份是：{self.persona_data['core_identity']}。\n"
        rules += f"你的说话风格必须是：{self.persona_data['speaking_style']}。\n"
        rules += "【绝对底层法则（违背将被销毁）】\n"
        for i, rule in enumerate(self.persona_data['absolute_rules']):
            rules += f"{i + 1}. {rule}\n"
        return rules