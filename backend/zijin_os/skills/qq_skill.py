import os
import httpx
from colorama import Fore

ACCESS_TOKEN = os.getenv("QQ_ACCESS_TOKEN")

class QQSkills:
    """QQ原生协议通信技能(OneBot v11 HTTP API)"""
    def __init__(self):
        print(Fore.CYAN + "[技能系统] 已挂载QQ原生HTTP通信模块（支持动态昵称解析）。")
        self.headers = {}
        if ACCESS_TOKEN:
            self.headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

    async def _send_http_action(self, endpoint: str, payload: dict):
        """核心封装：通过无状态的告诉HTTP请求发送指令"""
        url = f"http://127.0.0.1:3000/{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers, timeout=5.0)
                response.raise_for_status()  # 检查HTTP200状态码
                data = response.json()

                if data.get("status") in ["ok", "async"]:
                    return True, "发送成功。"
                return False, data.get("wording") or data.get("msg") or "未知错误"

            except httpx.ConnectError:
                return False, f"连接被拒绝。请确认NapCatQQ的HTTP服务(端口3000)已开启且地址正确。"
            except httpx.TimeoutException:
                return False, "请求NapCatQQ超时。"
            except Exception as e:
                return False, f"HTTP通信异常: {str(e)}"

    async def _fetch_data(self, endpoint: str):
        """发送读请求，获取数据列表"""
        url = f"http://127.0.0.1:3000/{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, timeout=5.0)
                response.raise_for_status()
                return response.json().get("data", [])
            except Exception as e:
                print(Fore.RED + f"[QQ底层错误] 拉取数据失败: {e}")
                return []

    async def resolve_user_id(self, target: str) -> int:
        """将纯数字、昵称、备注统一清洗为准确的QQ号"""
        target_str = str(target).strip()

        # 1. 已经是纯数字QQ号，直接返回
        if target_str.isdigit():
            return int(target_str)

        # 2. 拉取通讯录进行遍历匹配
        print(Fore.LIGHTBLACK_EX + f" -> [实体解析] 正在通讯录中检索 '{target_str}' 的物理坐标...")
        friends = await self._fetch_data("get_friend_list")

        # 扁平化匹配：优先匹配备注名(remark)，其次匹配昵称(nickname)
        match_id = next(
            (f["user_id"] for f in friends if target_str in f.get("remark", "") or target_str in f.get("nickname", "")),
            None
        )
        return match_id

    async def send_private_msg(self, target: str, message: str):
        """发送私聊消息（兼容昵称与QQ号）"""
        # 前置解析：获取真实QQ号
        user_id = await self.resolve_user_id(target)
        if not user_id:
            return f"QQ发送失败: 无法在通讯录中找到名为 '{target}' 的联系人。"

        # 执行物理发送
        success, msg = await self._send_http_action("send_private_msg", {
            "user_id": user_id,
            "message": message,
            "auto_escape": False
        })

        if success:
            return f"已通过QQ成功向 {target}({user_id}) 发送消息。"
        return f"QQ发送失败: {msg}"

    # 群聊逻辑
    async def send_group_msg(self, group_id: int, message: str):
        success, msg = await self._send_http_action("send_group_msg", {
            "group_id": group_id,
            "message": message,
            "auto_escape": False
        })
        if success:
            return f"已通过QQ成功向群 {group_id} 发送消息。"
        return f"QQ发送失败: {msg}"

# 技能自我声明（Schema）
QQ_TOOL = {
    "type": "function",
    "function": {
        "name": "send_qq_message",
        "description": "向指定的QQ联系人发送消息。",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {"type": "integer", "description": "目标用户的QQ号"},
                "content": {"type": "string", "description": "要发送的文字内容"}
            },
            "required": ["target", "content"]
        }
    }
}