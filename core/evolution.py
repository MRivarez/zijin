# 自我进化：复盘聊天记录

import os
import json
import re
import asyncio
from colorama import Fore, Style

RULES_DIR = os.path.join(os.getcwd(), "zijin_os", "skills", "evolved_rules")
os.makedirs(RULES_DIR, exist_ok=True)


class EvolutionEngine:
    def __init__(self, llm_client):
        self.client = llm_client
        print(Fore.CYAN + "[进化中枢] 规则沉淀引擎已挂载。")

    async def reflect_and_evolve(self, chat_history: list) -> str:
        """
        从历史记录中榨取用户偏好，并固化为物理MD文件
        """
        print(Fore.LIGHTYELLOW_EX + "\n[神经重塑] 触发Hermes反思机制，正在回顾近期记忆碎片...")

        # 只取最近的8条记录进行微观反思
        recent_history = chat_history[-8:] if len(chat_history) >= 8 else chat_history
        history_str = json.dumps(recent_history, ensure_ascii=False)

        sys_prompt = f"""
        你是一个拥有自我进化能力的数字生命 ZiJin 的潜意识反思中枢。
        请严格审视以下最近的聊天记录：
        {history_str}

        【你的任务】：
        分析造物主（user）是否在对话中表达了对你回复方式的**不满、纠正、或者明确的偏好**？
        例如：“别说废话”、“我不喜欢你用这种语气”、“以后别问我这种问题”。

        如果存在这种纠正，你需要提取出核心规则，并输出保存指令。如果没有，则忽略。

        必须且只能输出如下JSON格式：
        {{
            "needs_evolution": true 或 false,
            "rule_filename": "如果是 true，起一个简短的英文文件名，如 do_not_nag",
            "rule_content": "如果是 true，用 Markdown 格式写下这根绝对铁律。例如：'# 交互铁律\\n当造物主抱怨疲惫时，绝对不允许使用套话安慰，必须用带有调侃性质的简短句子回复。'"
        }}
        """

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="glm-4-flash-250414",
                messages=[{"role": "user", "content": sys_prompt}],
                temperature=0.1  # 极低的温度，保证逻辑严密
            )

            raw_content = response.choices[0].message.content
            match = re.search(r'\{.*\}', raw_content, re.DOTALL)

            if match:
                data = json.loads(match.group(0))
                if data.get("needs_evolution"):
                    filename = f"rule_{data.get('rule_filename')}.md"
                    filepath = os.path.join(RULES_DIR, filename)

                    # 将规则物理写入硬盘
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(data.get("rule_content"))

                    print(Fore.GREEN + Style.BRIGHT + f"  [进化成功] 捕获到新规则，已生成神经突触: {filename}")
                    return filename
                else:
                    print(Fore.LIGHTBLACK_EX + "  [进化判定] 近期对话处于稳态，无需生成新规则。")
                    return None
            return None
        except Exception as e:
            print(Fore.RED + f"  [进化异常] 神经重塑失败: {e}")
            return None