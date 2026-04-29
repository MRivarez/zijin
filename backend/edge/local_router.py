# 小脑：条件反射

from colorama import Fore

class CerebellumReflex:

    def __init__(self):
        print(Fore.CYAN + "[Cerebellum] 边缘小脑反射弧已挂载，接管基础动作反馈...")

        # 反射策略映射词典
        self.reflex_strategies = {
            "send_qq_message": self._reflex_qq_message,
            "send_wechat_message": self._reflex_wechat_message,
            # 未来如果有操作硬件、走步、抓取等底层动作，直接在这里增加映射
        }

    def generate_reflex(self, tool_name: str, action_result: str) -> str:
        """根据工具名称和执行结果，瞬间生成拟人化反馈"""

        # 提取策略函数，如果没有对应策略，返回None让大脑接管
        strategy_func = self.reflex_strategies.get(tool_name)
        if not strategy_func:
            return None

        return strategy_func(action_result)

    def _reflex_qq_message(self, result: str) -> str:
        """QQ发送动作的极速反射"""
        res_str = str(result)
        if "成功" in res_str:
            return "脑电波已通过QQ链路成功发射！"
        if "无法在通讯录中找到" in res_str:
            return "糟糕，发送失败了。我的QQ通讯录里好像没有这个人，你确定名字没打错吗？"
        return f"QQ链路出现异常波动：{res_str}"

    def _reflex_wechat_message(self, result: str) -> str:
        """微信发信的极速反射"""
        res_str = str(result)
        if "成功" in res_str:
            return "搞定啦！微信消息已经盲发出去啦。"
        return "微信发送似乎卡住了，请检查一下屏幕焦点哦。"