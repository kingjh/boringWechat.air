# -*- encoding=utf8 -*-
# 特殊处理：这段初始化的代码。由AirtestIDE生成，在执行脚本时要确保手机连上电脑，并确保「adb」命令正常运行
# 特殊处理start
from airtest.core.api import *
# 执行结束后目前会自动有个停顿时间OPDELA，默认0.1s。以下把停顿时间设置为0
from airtest.core.settings import Settings as ST
ST.OPDELAY = 0
auto_setup(__file__)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
# 特殊处理end

# 打开手机微信
wechat_btn = poco(text="微信")
if wechat_btn.exists():
    wechat_btn.click()

# 以下部分请用main.py里面要测试的def替换
# 替换start
while True:
    # 群聊消息的元素标识。
    # 特殊处理：以下poco里的“id/”后的字母，在不同手机型号中可能不同
    chat_objs = poco("com.tencent.mm:id/b9k")
    # 获取当前页面中所有群聊的最新消息
    chats = list(chat_objs)
    for i in range(0, len(chats) - 1):
        if chat_objs[i].get_text().find("[微信红包]") != -1:
            # 点击进入最新消息是红包的群聊
            chat_objs[i].click()
            # 在微信聊天页面中，获取当前聊天中的所有元素
            msg_objs = poco("android.widget.FrameLayout").children()
            for msg_obj in msg_objs:
                # 微信红包的标识
                red_pocket_obj = msg_obj.offspring("com.tencent.mm:id/asm")

                # 判断红包是否有效并抢起来！
                if red_pocket_obj:
                    # 已失效红包（比如已领取、已被领完）的标识
                    status_obj = msg_obj.offspring("com.tencent.mm:id/aso")
                    if status_obj.exists() and (status_obj.get_text() == "已领取" or status_obj.get_text() == "已被领完"):
                        print(f"红包已无效，跳过……")
                        continue
                    else:
                        print(f"发现一个新红包，抢起来！")
                        msg_obj.click()
                        open_btn = poco("android.widget.FrameLayout").offspring("com.tencent.mm:id/d5a")
                        if open_btn.exists():
                            open_btn.click()
                        keyevent("BACK")

            keyevent("BACK")
# 替换部分end