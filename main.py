# -*- encoding=utf8 -*-
import sys

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

# 特殊处理：每一个def请先放在boringWechat.py里面，用AirtestIDE独立测试，测试好再放在main.py里面
def red_pocket():
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


def like():
    discovery_btn = poco(text="发现")
    if discovery_btn.exists():
        discovery_btn.click()

    friend_circle_btn = poco(text="朋友圈")
    # get_name保证“朋友圈”是在第一级界面的朋友圈入口，而不是进入朋友圈后的标题
    if friend_circle_btn.exists() and friend_circle_btn.get_name().find("android:id/title") != -1:
        # 在朋友圈外，进入朋友圈
        friend_circle_btn.click()
        time.sleep(0.1)
        # 等待朋友圈刷新完毕
        # 特殊处理：以下poco里的“id/”后的字母，在不同手机型号中可能不同
        refresh_circle = poco("com.tencent.mm:id/euu")
        refresh_circle.wait_for_disappearance(30)
    elif friend_circle_btn.exists():
        # 在朋友圈内且有“朋友圈”三个字，意味着不在顶部，需要回到顶部
        # 特殊处理：poco的双击未实现，用airtest双击回顶
        double_click(Template(r"tpl1566012446106.png", record_pos=(-0.323, -0.76), resolution=(1080, 1920)))
        time.sleep(0.1)
        # 特殊处理：以下poco里的“id/”后的字母，在不同手机型号中可能不同
        refresh_circle = poco("com.tencent.mm:id/euu")
        # 当有新信息时，刷新的圆圈会exists，这时需要等待；否则圆圈转瞬即逝，无需等待
        if refresh_circle.exists():
            # 等待朋友圈刷新完毕
            refresh_circle.wait_for_disappearance()
    else:
        # 在朋友圈顶部，假定已更新所有信息，不做刷新
        pass

    name_obj = poco("com.tencent.mm:id/b9i")
    if name_obj.exists():
        name = name_obj.get_text()
    else:
        name = False

    while True:
        # 在朋友圈页面中，获取所有条目
        msg_objs = poco("com.tencent.mm:id/eu7")
        msgs = list(msg_objs)
        for i in range(0, len(msgs) - 1):
            # 在朋友圈页面中，获取当前条目的所有元素
            like_obj = msg_objs[i].offspring("com.tencent.mm:id/etu")
            if not name or not like_obj.exists() or like_obj.get_text().find(name) == -1:
                # 如果拿不到当前用户昵称，或未点过赞，点赞
                popup_btn = msg_objs[i].offspring("com.tencent.mm:id/eop")
                if popup_btn.exists():
                    popup_btn.click()
                    time.sleep(0.1)
                    poco("com.tencent.mm:id/eob").click()

        scroll_view_obj = poco("com.tencent.mm:id/epj")
        scroll_view_obj.swipe([0, -0.8])


def main():
    if len(sys.argv) <= 1:
        sys.exit("请输入处理模式")

    # 打开手机微信
    # 特殊处理：请保证打开微信后，当前位置是微信的一级菜单（底部按钮是：微信、通讯录、发现、我，的那一级菜单）
    wechat_btn = poco(text="微信")
    if wechat_btn.exists():
        wechat_btn.click()

    switch = {
        "0": red_pocket,
        "1": like,
    }
    switch[sys.argv[1]]()


if __name__ == "__main__":
    main()
