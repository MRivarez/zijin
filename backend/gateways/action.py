# 肢体：OpenClaw执行网关 负责所有物理输出

import json
import asyncio
from colorama import Fore
from zijin_os.skills.qq_skill import QQSkills, QQ_TOOL
from zijin_os.skills.wechat_fallback import WeChatUiaSkills, WECHAT_TOOL


class ActionGateway:
    def __init__(self):
        print(Fore.LIGHTBLACK_EX + "正在初始化跨协议动作网关（动态插件注册）...")
        # 初始化QQ技能
        self.qq_skill = QQSkills()
        if WeChatUiaSkills is not None:
            self.wechat_skill = WeChatUiaSkills()
        else:
            self.wechat_skill = None

    async def dispatch(self, tool_call):
        """分发大脑的工具调用意图"""
        name = tool_call["name"]
        args = json.loads(tool_call["arguments"])

        target = args.get("target")
        content = args.get("content")

        if name == "send_qq_message":
            print(Fore.CYAN + f" -> [动作路由] 匹配到QQ协议，正在调用NapCatQQ网关...")
            # 确保传入的是数字类型的QQ号
            return await self.qq_skill.send_private_msg(target, content)

        elif name == "send_wechat_message":
            if self.wechat_skill is not None:
                print(Fore.YELLOW + f" -> [动作路由] 匹配到微信协议，正在调用UIA物理触手...")
                # UIA脚本包含阻塞逻辑，实际调用时仍在main.py的to_thread中运行以保安全
                return await asyncio.to_thread(self.wechat_skill.send(str(target), content))
            else:
                print("[网关跳过] 微信自动化模块因环境限制，未接入总线。")

        else:
            return f"网关错误：未知的技能调用 '{name}'"

# 统一的大脑工具定义 (Tool Schema)
REGISTERED_ACTION_TOOLS = [
    QQ_TOOL
]
if WECHAT_TOOL is not None:
    REGISTERED_ACTION_TOOLS.append(WECHAT_TOOL)
else:
    print("[网关跳过] 微信自动化模块因环境限制，未接入总线。")