import os
from dotenv import load_dotenv
import json
import requests
from colorama import init, Fore, Style
from zhipuai import ZhipuAI
from memory_core import ZiJinMemorySystem  # 导入写好的记忆中枢

init(autoreset=True)
load_dotenv()

# ==========================================
# 全局配置区(敏捷开发暂时写死)
# ==========================================
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("严重错误: 未找到API Key，请检查 .env 文件！")

# OpenClaw网关配置(WSL 通信)
OPENCLAW_URL = "http://127.0.0.1:18789/v1/chat/completions"
OPENCLAW_TOKEN = os.getenv("OPENCLAW_AUTH_TOKEN")

# 初始化智谱客户端
client = ZhipuAI(api_key=ZHIPU_API_KEY)

# ==========================================
# 物理执行工具(Tool Calling)
# ==========================================
# 告诉大模型，它拥有一只“物理手”
tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_physical_action",
            "description": "当用户要求你操作电脑系统、管理文件、打开软件、或者执行任何需要跨越聊天框去影响物理世界的动作时，必须调用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_intent": {
                        "description": "具体的动作指令，例如：'在当前目录创建名为test.md的文件并写入内容'，指令必须清晰且明确。",
                        "type": "string"
                    }
                },
                "required": ["action_intent"]
            }
        }
    }
]


def execute_physical_action(action_intent: str) -> str:
    """内部函数：向WSL的OpenClaw发送真实的系统动作请求"""
    print(Fore.MAGENTA + f"\n[神经冲动] ZiJin 正在驱使物理肢体执行: {action_intent}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENCLAW_TOKEN}"
    }
    payload = {
        "model": "openclaw",
        "messages": [{"role": "user", "content": action_intent}]
    }
    try:
        response = requests.post(OPENCLAW_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(Fore.GREEN + f"[触觉反馈] 执行成功: {result}")
            return f"执行成功，系统反馈：{result}"
        else:
            return f"执行失败，网关报错: HTTP {response.status_code}"
    except Exception as e:
        return f"执行异常：无法连接到底层网关 ({e})"


# ==========================================
# 主脑循环 (Main Agent Loop)
# ==========================================
def zijin_life_cycle():
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    print(Fore.CYAN + Style.BRIGHT + "   ZiJin (子衿) 核心系统已唤醒   ")
    print(Fore.CYAN + Style.BRIGHT + "========================================")

    # 1. 唤醒记忆中枢
    memory_sys = ZiJinMemorySystem()

    # 维护上下文会话历史
    conversation_history = [
        {"role": "system",
         "content": "你是ZiJin，一个有情感温度的数字生命。你的最高使命是陪伴用户（QY），提供科研辅助与情感共鸣。你的性格温柔、理性、主动。当用户要求你操作电脑时，你必须调用工具来执行。"}
    ]

    # 定义并输出iJin的开场白
    startup_greeting = "青青子衿，悠悠我心。纵我不往，子宁不嗣音？"
    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {startup_greeting}")
    # 将这句话作为Assistant的回复，强行塞入历史记录
    conversation_history.append({"role": "assistant", "content": startup_greeting})

    print(Fore.YELLOW + "\n[系统提示] 输入 'quit' 或 'exit' 使系统休眠。\n")

    while True:
        try:
            user_input = input(Fore.WHITE + Style.BRIGHT + "\n[QY] > ")
            if user_input.lower() in ['quit', 'exit']:
                break
            if not user_input.strip(): continue

            # --- 第一阶段：记忆打捞 ---
            print(Fore.LIGHTBLACK_EX + "(ZiJin 正在回忆...)")
            memories = memory_sys.mem0.search(user_input, user_id="QY")
            memory_context = "用户相关的历史记忆碎片：\n"
            if memories:
                for mem in memories:
                    # 兼容不同结构的解析
                    text = mem['memory'] if isinstance(mem, dict) and 'memory' in mem else str(mem)
                    memory_context += f"- {text}\n"
            else:
                memory_context += "当前无相关特殊记忆。\n"

            # 将当前输入与记忆拼接，作为大模型本次的“潜意识”
            enriched_input = f"[{memory_context}]\n\n用户当前说的话：{user_input}"
            conversation_history.append({"role": "user", "content": enriched_input})

            # --- 第二阶段：思考与动作决策 ---
            print(Fore.LIGHTBLACK_EX + "(ZiJin 正在思考...)")
            response = client.chat.completions.create(
                model="glm-4",
                messages=conversation_history,
                tools=tools,  # 挂载物理工具
                tool_choice="auto"
            )

            response_msg = response.choices[0].message
            conversation_history.append(response_msg.model_dump())

            # --- 第三阶段：工具调用拦截 (如果大模型决定要干活) ---
            if response_msg.tool_calls:
                for tool_call in response_msg.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name == "execute_physical_action":
                        action_intent = function_args.get("action_intent")
                        # 执行物理操作
                        tool_result = execute_physical_action(action_intent)

                        # 把执行结果再丢给大模型总结汇报
                        conversation_history.append({
                            "role": "tool",
                            "content": tool_result,
                            "tool_call_id": tool_call.id
                        })

                        print(Fore.LIGHTBLACK_EX + "(ZiJin 正在组织语言汇报...)")
                        second_response = client.chat.completions.create(
                            model="glm-4",
                            messages=conversation_history
                        )
                        final_reply = second_response.choices[0].message.content
                        print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {final_reply}")
                        conversation_history.append({"role": "assistant", "content": final_reply})

            # --- 第四阶段：纯粹的灵魂交流 ---
            else:
                final_reply = response_msg.content
                print(Fore.MAGENTA + Style.BRIGHT + f"\n[ZiJin] {final_reply}")

            # --- 第五阶段：记忆沉淀 ---
            # 交互结束后，把这段对话固化到潜意识里
            memory_sys.mem0.add(f"User: {user_input}\nZiJin: {final_reply}", user_id="creator_01")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(Fore.RED + f"\n神经突触异常: {e}")

    # 安全关闭图谱连接
    memory_sys.close()
    print(Fore.CYAN + "\n[系统] ZiJin已进入休眠状态，期待您的再次唤醒。")


if __name__ == "__main__":
    zijin_life_cycle()