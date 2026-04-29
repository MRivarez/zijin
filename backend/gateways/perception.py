import sys
import logging
import time
import asyncio
import json
import websockets
from colorama import Fore, Style

import os
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("QQ_ACCESS_TOKEN")

class NapCatPerception:
    """QQ听觉神经——基于WebSocket持续监听OneBot v11事件"""

    def __init__(self, ws_url: str = "ws://napcat:3001", creator_qq: str = ""):
        # 默认NapCatQQ的WebSocket端口为3001
        self.ws_url = ws_url
        self.creator_qq = str(creator_qq)
        # 鉴权组装
        self.headers = {}
        if ACCESS_TOKEN:
            self.headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
        print(Fore.CYAN + "[感知网关] NapCatQQ听觉神经已初始化，准备接入...")

    async def listen(self, stimulus_queue: asyncio.Queue):
        """常驻协程：维持WS隧道并转化神经脉冲"""
        print(Fore.YELLOW + f" -> [感知网关] 尝试连接QQ脑机接口: {self.ws_url}")

        while True:
            try:
                async with websockets.connect(self.ws_url, additional_headers=self.headers, ping_interval=None, ping_timeout=None) as websocket:
                    print(Fore.GREEN + "  ✅ [感知网关] 脑机接口连接成功！正在全天候监听造物主消息...")

                    while True:
                        msg = await websocket.recv()
                        data = json.loads(msg)

                        # 1. 忽略OneBot的meta_event(如每秒的心跳包，防止日志刷屏)
                        if data.get("post_type") == "meta_event":
                            continue

                        # 2. 只处理私聊消息
                        if data.get("post_type") != "message" or data.get("message_type") != "private":
                            continue

                        sender_id = str(data.get("user_id"))

                        # 3. 只理会造物主的消息，无视其他人或群聊的干扰
                        if sender_id != self.creator_qq:
                            print(Fore.LIGHTBLACK_EX + f"    [感知拦截] 忽略来自({self.creator_qq})而非造物主({sender_id})的杂音。")
                            continue

                        raw_text = data.get("raw_message", "").strip()
                        if raw_text:
                            print(Fore.MAGENTA + Style.BRIGHT + f"\n[QQ 传入刺激] {raw_text}")

                            # 转化为标准的神经脉冲，打入主系统队列
                            # 这将瞬间唤醒cognitive_loop进行大模型坍缩
                            await stimulus_queue.put(("user", raw_text))

            except websockets.exceptions.ConnectionClosed as e:
                print(Fore.RED + f" -> [感知网关] QQ隧道意外断开 ({e})，5秒后启动自愈重连...")
                await asyncio.sleep(5)
            except Exception as e:
                print(Fore.RED + f" -> [感知网关] 听觉神经发生未知异常: {e}，5秒后重试...")
                await asyncio.sleep(5)

if sys.platform == "win32":
    import uiautomation as auto
    class NativeUIAPerception:
        def __init__(self):
            print(Fore.LIGHTBLACK_EX + "正在初始化原生UIA神经中枢(WeChat4.1属性级提取版)...")
            self.processed_msg_fingerprints = set()

        def watch_screen(self, on_new_message_callback):
            print(Fore.CYAN + "[感知层] 正在基于List(50008)属性静默扫描新消息...")

            # 保持COM多线程隔离安全
            with auto.UIAutomationInitializerInThread():
                wechat_win = auto.WindowControl(Name='微信')

                while True:
                    try:
                        if not wechat_win.Exists(0, 0):
                            time.sleep(1.0)
                            continue

                        # 1. 严格按照查出的属性定位：Name="消息", ControlType=List(50008)
                        msg_list = wechat_win.ListControl(Name='消息', searchDepth=15)

                        if msg_list.Exists(0, 0):
                            # 2. 获取所有的ListItem
                            items = msg_list.GetChildren()
                            if items:
                                # 处理最后5条消息，防止连续发送时被漏掉
                                msg_list_rect = msg_list.BoundingRectangle
                                # 计算聊天界面的垂直中心线
                                center_x = (msg_list_rect.left + msg_list_rect.right) / 2 if msg_list_rect else 0

                                for item in items[-5:]:
                                    content = item.Name
                                    if not content:
                                        continue

                                    sender = "对方"
                                    # 遍历查找头像按钮，通过其位置判断是自己发的还是别人发的
                                    for child in item.GetChildren():
                                        if child.ControlType == auto.ControlType.ButtonControl:
                                            btn_rect = child.BoundingRectangle
                                            # 如果头像在屏幕右半侧，那绝对是“自己”
                                            if center_x > 0 and btn_rect and btn_rect.left > center_x:
                                                sender = "自己"
                                            elif child.Name:
                                                sender = child.Name
                                            break

                                    fingerprint = f"{sender}_{content}_{item.BoundingRectangle.top}"

                                    # 过滤掉已处理的消息
                                    if fingerprint not in self.processed_msg_fingerprints:
                                        self.processed_msg_fingerprints.add(fingerprint)
                                        # 我们不回应自己发出的消息，避免死循环
                                        if sender not in ["自己"]:
                                            print(Fore.GREEN + Style.BRIGHT + f"[新消息捕获] {sender}: {content}")
                                            # 将刺激打入ZiJin的主脑队列
                                            on_new_message_callback(f"{sender} 发来消息: {content}")

                    except Exception:
                        # 忽略UI刷新时的偶发异常
                        pass

                    time.sleep(1.0)

else:
    # Docker(Linux)的空壳感知器
    class NativeUIAPerception:
        def __init__(self, *args, **kwargs):
            logging.warning("⚠️ [感知降级]非Windows环境，微信监听已处于休眠状态。")