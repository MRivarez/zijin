# Mano-P 微信自动化驱动

import uiautomation as auto
import time
from colorama import Fore, Style

def trigger_wechat_message(target_name: str, message: str) -> str:
    """
    核心动作：利用全局快捷键劫持微信并发送消息
    """
    print(Fore.MAGENTA + f"\n[Mano-P物理操纵] 正在尝试唤醒微信并联系: {target_name}...")

    try:
        # 1. 无论微信在哪，发送全局唤醒快捷键强行拉起
        # 默认是Ctrl+Alt+W。如果微信改了快捷键，请修改这里。
        auto.SendKeys('{Ctrl}{Alt}w')
        time.sleep(1.0)  # 给予UI渲染和弹出的时间

        # 2. 寻找主窗口，增加 searchDepth=1 (只在顶层窗口找)，极大提升搜索速度和命中率
        print("开始寻找微信主窗口......")
        wechat_win = auto.WindowControl(searchDepth=1, Name='微信', ClassName='Qt51514QWindowIcon')
        if wechat_win.Exists(0, 0):
            print("-> 发现微信已存在于桌面，直接激活。")
        else:
            # 强制回到桌面，放置pycharm拦截快捷键
            auto.SendKeys('{Win}d')
            time.sleep(0.5)
            print(" -> 尝试通过全局快捷键唤醒微信...")
            auto.SendKeys('{Ctrl}{Alt}w')
            if not wechat_win.Exists(5, 1):
                return ("执行失败：无法捕捉微信窗口。请排查："
                    "1.微信是否已登录并运行；"
                    "2.是否修改了微信默认的打开快捷键(Ctrl+Alt+W)；"
                    "3.请尝试以【管理员身份】重新运行当前的Python终端。")

        # 3. 强行获取焦点
        print("聚焦到微信主窗口")
        wechat_win.SetActive()
        time.sleep(0.5)

        # 4. 搜索定位
        print(Fore.CYAN + "[Mano-P 内部状态] 正在模拟Ctrl+F唤出搜索框...")
        auto.SendKeys('{Ctrl}f')
        time.sleep(0.3)

        # 5. 注入联系人
        print(Fore.CYAN + f"[Mano-P 内部状态] 正在输入联系人: {target_name}")
        auto.SetClipboardText(target_name)
        auto.SendKeys('{Ctrl}v')
        time.sleep(1.0)  # 等待列表渲染出这个人的ListItem

        # 6. 回车进入聊天流
        print(Fore.CYAN + "[Mano-P 内部状态] 已锁定目标，敲击回车进入对话...")
        auto.SendKeys('{Enter}')
        time.sleep(0.5)

        # 7. 注入消息
        print("[Mano-P 内部状态] 正在注入消息......")
        auto.SetClipboardText(message)
        auto.SendKeys('{Ctrl}v')
        time.sleep(0.2)
        auto.SendKeys('{Enter}')

        # 8. 发完消息后，再次按下快捷键把微信隐藏
        # auto.SendKeys('{Ctrl}{Alt}w')

        print(Fore.GREEN + "[Mano-P 触觉反馈] 消息物理投递成功，已切回静默状态。")
        return f"已成功通过微信向 {target_name} 发送了消息。"

    except Exception as e:
        print(Fore.RED + f"[Mano-P故障] 自动化流异常: {e}")
        return f"执行失败：UI自动化介入时发生异常 ({e})"