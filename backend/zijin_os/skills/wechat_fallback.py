import sys
import logging
# 判断当前操作系统
if sys.platform == "win32":
    import uiautomation as auto
    import time
    import pyperclip
    import pyautogui
    import ctypes
    from colorama import Fore, Style
    class WeChatUiaSkills:
        """微信UIA自动化技能 (降级备选方案)"""

        def __init__(self):
            print(Fore.LIGHTBLACK_EX + "正在初始化原生UIA动作网关 (热键基线 + 焦点夺取线程安全强控版)...")

        @staticmethod
        def send_message(self, target_name: str, message_content: str):
            # 为当前子线程动态注入COM初始化上下文
            with auto.UIAutomationInitializerInThread():
                wechat_win = auto.WindowControl(Name='微信', ClassName='mmui::MainWindow')
                if not wechat_win.Exists(1, 1):
                    wechat_win = auto.WindowControl(Name='微信', ClassName='WeChatMainWndForPC')

                if not wechat_win.Exists(1, 1):
                    return "执行失败：无法在底层找到微信主窗口。"

                print(Fore.MAGENTA + Style.BRIGHT + f"\n[原生 UIA 执行] 目标: {target_name} | 内容: {message_content}")

                try:
                    # 1. 物理置顶窗口的终极方法
                    hwnd = wechat_win.NativeWindowHandle

                    # 解决第一次运行焦点抢不过来的Bug: AttachThreadInput强行附加输入上下文
                    foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
                    if foreground_hwnd != hwnd and foreground_hwnd != 0:
                        foreground_thread = ctypes.windll.user32.GetWindowThreadProcessId(foreground_hwnd, 0)
                        app_thread = ctypes.windll.kernel32.GetCurrentThreadId()
                        if foreground_thread != app_thread:
                            ctypes.windll.user32.AttachThreadInput(foreground_thread, app_thread, True)
                            ctypes.windll.user32.BringWindowToTop(hwnd)
                            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                            ctypes.windll.user32.SetForegroundWindow(hwnd)
                            ctypes.windll.user32.AttachThreadInput(foreground_thread, app_thread, False)
                    else:
                        if ctypes.windll.user32.IsIconic(hwnd):
                            ctypes.windll.user32.ShowWindow(hwnd, 9)
                        ctypes.windll.user32.SetForegroundWindow(hwnd)

                    # 使用系统底层的强行提权
                    ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
                    wechat_win.SetTopmost(True)
                    time.sleep(0.3)

                    # 物理点击微信标题栏确立绝对焦点
                    # 从PyCharm启动时，Windows防焦点偷取机制极有可能把快捷键吞在终端里
                    wechat_rect = wechat_win.BoundingRectangle
                    if wechat_rect:
                        pyautogui.click(wechat_rect.left + 150, wechat_rect.top + 15)
                        time.sleep(0.3)

                    # 直接点亮特定聊天节点与输入框
                    # 完全抛弃坐标计算盲打，改为基于Accessibility语义控制
                    print(Fore.CYAN + " -> [语义寻址] 正在使用纯控件属性检索...")

                    # 第一重保障：尝试在左侧"会话"列表中直接查找此人
                    session_list = wechat_win.ListControl(Name="会话")
                    if session_list.Exists(0.5):
                        target_item = session_list.ListItemControl(Name=target_name)
                        if target_item.Exists(0.5):
                            print(Fore.GREEN + f" -> [左侧列表命中] 找到了 {target_name} 的独立会话控件，执行物理点击.")
                            target_item.Click(simulateMove=False)
                            time.sleep(0.3)

                    # 由于可能处于群组或不在近期会话，为了绝对兜底，依然附带一次搜索流程
                    search_box = wechat_win.EditControl(Name="搜索")
                    if search_box.Exists(0.5):
                        print(Fore.CYAN + " -> [主动搜索命中] 获取到了搜索框，准备键入。")
                        search_box.Click(simulateMove=False)
                        time.sleep(0.1)
                        pyperclip.copy(target_name)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.8)
                        pyautogui.press('enter')
                        time.sleep(0.5)
                    else:
                        # 回退盲切
                        pyautogui.hotkey('ctrl', 'f')
                        time.sleep(0.2)
                        pyperclip.copy(target_name)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.8)
                        pyautogui.press('enter')
                        time.sleep(0.5)

                    # 定位聊天输入框，聊天输入框的Name是联系人名字
                    chat_input = wechat_win.EditControl(Name=target_name)

                    if chat_input.Exists(1.0):
                        print(Fore.GREEN + f" -> 成功抓取到底层专属输入控件 (Name='{target_name}').")
                        # 使用uiautomation提供的Click对象直接控制鼠标去点击它暴露的BoundingRectangle
                        chat_input.Click(simulateMove=False)
                        time.sleep(0.2)
                    else:
                        print(
                            Fore.YELLOW + " -> [警告] 未能通过严格的名称属性找到对应的Edit控件，执行兜底：定位最底端输入框...")
                        edits = []
                        # 限制寻找在界面内的未命名或命名为"输入"的框
                        # 在没有Name的情况下还是需要使用老办法防呆
                        for ctrl in wechat_win.GetChildren():
                            if ctrl.ControlType == auto.ControlType.EditControl:
                                edits.append(ctrl)
                            for child in ctrl.GetChildren():
                                if child.ControlType == auto.ControlType.EditControl:
                                    edits.append(child)

                        if edits:
                            valid_edits = [e for e in edits if e.BoundingRectangle]
                            if valid_edits:
                                valid_edits.sort(key=lambda x: x.BoundingRectangle.top)
                                valid_edits[-1].Click(simulateMove=False)
                                time.sleep(0.2)

                    # 3. 注入内容并发送 (基线验证成功的逻辑)
                    pyperclip.copy(message_content)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.2)
                    pyautogui.press('enter')

                    wechat_win.SetTopmost(False)
                    print(Fore.GREEN + "[执行完毕] 发送动作已闭环！")
                    return f"已成功向 {target_name} 发送消息。"

                except Exception as e:
                    wechat_win.SetTopmost(False)
                    print(Fore.RED + f"[底层执行异常] {e}")
                    return f"系统级发送失败: {e}"


    WECHAT_TOOL = {
        "type": "function",
        "function": {
            "name": "send_wechat_message",
            "description": "通过底层UIA协议向指定的微信联系人发送文字消息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_name": {"type": "string", "description": "微信联系人昵称或备注"},
                    "message_content": {"type": "string", "description": "要发的文字内容"}
                },
                "required": ["target_name", "message_content"]
            }
        }
    }

else:
    logging.warning("[系统降级]当前环境非Windows，微信自动化触觉已切断。")


    # 伪造一个空壳类，方法名和你原来一样，防止其他地方调用时崩溃
    class WeChatUiaSkills:
        def __init__(self):
            pass

        def send_message(self, *args, **kwargs):
            logging.error("无法执行：当前系统未搭载 Windows 微信模块。")
            return "Failed: 微信模块在当前容器中不可用"


    # 将工具设为None，作为给上一级（Gateway）的降级信号
    WECHAT_TOOL = None