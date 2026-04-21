import time

import uiautomation as auto

print("正在解析当前系统的底层 UI 树...")
desktop = auto.GetRootControl()

# 遍历桌面下的所有顶层窗口
# for win in desktop.GetChildren():
#     if win.ControlType == auto.ControlType.WindowControl:
#         name = win.Name
#         class_name = win.ClassName
#         # 过滤掉无用的空窗口，只打印有名字的
#         if name:
#             print(f"窗口名称: [{name}]  --->  底层 ClassName: [{class_name}]")

import uiautomation as auto
# 扫描鼠标当前指向的控件（把鼠标放在搜出来的那个联系人上运行）
while(True):
    control = auto.ControlFromCursor()
    print(f"真实的底层名字是: [{control.Name}]，控件类型是: [{control.ControlType}]")
    time.sleep(1)