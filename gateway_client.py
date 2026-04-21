import requests
import json
from colorama import Fore, Style

# 替换为WSL虚拟网卡真实IP
WSL_IP = "172.21.208.5"
OPENCLAW_PORT = 18789  # OpenClaw 默认暴露端口
API_URL = f"http://{WSL_IP}:{OPENCLAW_PORT}/api/v1/agent/execute"


def execute_action_via_openclaw(instruction):
    print(Fore.CYAN + f"[ZiJin 中枢神经] 正在向下层动作网关下发指令: {instruction}")

    payload = {
        "command": instruction,
        "mode": "autonomous",  # 允许OpenClaw根据大模型推演自行拆解底层系统级动作
        "max_steps": 5  # 强制设定状态机步数上限，避免逻辑死锁
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        result = response.json()
        print(Fore.GREEN + "[动作执行层反馈]: \n" + json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[致命错误]无法建立与OpenClaw动作节点的套接字连接: {e}")
        return None


if __name__ == "__main__":
    # 执行一条具备强验证性且物理隔离的安全系统命令
    execute_action_via_openclaw(
        "在当前Linux用户的home目录下创建一个名为zijin_heartbeat.txt 的文件，并向其中写入文本内容：'青青子衿，悠悠我心'。")