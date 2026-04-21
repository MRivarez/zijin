import os
from dotenv import load_dotenv
import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

# 依赖WSL2自动端口转发
WSL_IP = "127.0.0.1"
OPENCLAW_PORT = 18789
GATEWAY_TOKEN = os.getenv("GATEWAY_TOKEN")

# 指向OpenClaw真正对外暴露的兼容OpenAI协议端点
API_URL = f"http://{WSL_IP}:{OPENCLAW_PORT}/v1/chat/completions"


def execute_zijin_action():
    print(Fore.CYAN + "[ZiJin 执行网关] 正在通过兼容协议向物理层下发指令...\n")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GATEWAY_TOKEN}"
    }

    # 按照OpenAI SDK的标准Payload格式进行组装
    payload = {
        "model": "openclaw",  # 显式指定请求处理方为 OpenClaw 的主 Agent
        "messages": [
            {
                "role": "user",
                "content": "请在当前目录（zijin-os）下，创建一个名为'hello_zijin.md'的文件，并写入文本：'这是ZiJin突破系统次元壁的第一道痕迹。'"
            }
        ]
    }

    try:
        # Agent 执行物理动作可能耗时较长，增加超时时间
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)

        if response.status_code == 200:
            result = response.json()
            # 提取Agent经过思考与执行完毕后的最终回复
            agent_reply = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(Fore.GREEN + f"✅ 执行成功！底层网关反馈：\n{agent_reply}")
        elif response.status_code == 401:
            print(Fore.RED + "❌ 鉴权失败：Token 被拒绝。")
        else:
            print(Fore.RED + f"❌ 意外报错 (HTTP {response.status_code}):\n{response.text}")

    except requests.exceptions.ConnectionError:
        print(Fore.RED + "❌ 连接失败：端口被拒绝，请确认 openclaw dashboard 已重新拉起。")
    except Exception as e:
        print(Fore.RED + f"❌ 未知异常：{e}")


if __name__ == "__main__":
    execute_zijin_action()