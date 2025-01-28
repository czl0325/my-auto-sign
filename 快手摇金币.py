import random
import re

import uiautomator2 as u2
import time
from utils import find_button

d = u2.connect()
screen_width, screen_height = d.window_size()
d.app_start("com.kuaishou.nebula", stop=True)
ctx = d.watch_context()
ctx.when(xpath='//*[@resource-id="com.kuaishou.nebula:id/popup_view"]//*[@resource-id="com.kuaishou.nebula:id/close_btn"]').click()
ctx.when("立即签到").click()
ctx.when("看内容最高可得1000金币").click()
ctx.when("领取奖励").click()
ctx.when("开心收下").click()
ctx.when("刷新").click()
ctx.start()
time.sleep(5)


def close_dialog():
    try_count = 1
    while try_count > 0:
        pt = find_button(d.screenshot(format='opencv'), "./kuaishou/ks-close.png")
        if pt:
            d.click(int(pt[0]) + 10, int(pt[1]) + 10)
            time.sleep(2)
            break
        time.sleep(4)
        try_count -= 1


def back_to_foca_main():
    while True:
        if d(className="android.view.View", text="做任务 领福卡").exists:
            break
        d.press("back")
        time.sleep(0.2)


def operate_photo_detail():
    if d(className="android.view.View", text="做任务 领福卡").exists:
        print("当前在任务页面，退出")
        return
    while True:
        # 左上角类型
        time_div2 = d(resourceId="com.kuaishou.nebula.commercial_neo:id/video_countdown", className="android.widget.TextView")
        if time_div2.exists(timeout=3):
            time_text = time_div2.get_text()
            print(f"属于左上角类型,获取到的时间是:{time_text}")
            match = re.search(r"(\d+)s后可领取奖励", time_text)
            if match:
                time_text = match.group(1)
                time.sleep(int(time_text) + 5)
            d.click(time_div2.center()[0], time_div2.center()[1])
            time.sleep(5)
            next_btn = d(resourceId="com.kuaishou.nebula.commercial_neo:id/again_medium_icon_dialog_ensure_text", text="领取奖励")
            if next_btn.exists:
                next_btn.click()
                time.sleep(5)
                continue
            else:
                break
        # 右上角小图标类型
        time_div1 = d(className="android.widget.TextView", resourceId="com.kuaishou.nebula:id/neo_count_down_text")
        time_div4 = d(className="android.widget.TextView", resourceId="com.kuaishou.nebula:id/pendant_task_status")
        if time_div1.exists(timeout=3) or time_div4.exists(timeout=3):
            time_text = time_div1.get_text() if time_div1.exists else time_div4.get_text()
            print(f"属于右上角小图标时间类型,获取到的时间是:{time_text}")
            if ":" in time_text:
                sleep_time = int(time_text.split(":")[1])
                print(f"开始睡眠{sleep_time + 5}秒")
                time.sleep(sleep_time + 5)
                dialog = d(resourceId="com.kuaishou.nebula:id/krn_content_container", className="android.widget.FrameLayout")
                print(f"是否有弹窗存在:{dialog.exists}")
                if dialog.exists:
                    d.click(dialog.center()[0], dialog.bounds()[1] - 20)
                    time.sleep(3)
                # com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container
                close_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container", className="android.widget.FrameLayout")
                print(f"右上角关闭按钮是否存在:{close_btn.exists}")
                if close_btn.exists:
                    d.click(close_btn.center()[0], close_btn.center()[1])
                    time.sleep(3)
                exit_btn = d(className="android.widget.TextView", textMatches=r"退出直播间|退出")
                print(f"退出直播间按钮是否存在:{exit_btn.exists}")
                if exit_btn.exists:
                    d.click(exit_btn.center()[0], exit_btn.center()[1])
                    time.sleep(5)
                next_btn = d(resourceId="com.kuaishou.nebula.commercial_neo:id/again_medium_icon_dialog_ensure_text", text="领取奖励")
                print(f"领取奖励按钮是否存在:{next_btn.exists}")
                if next_btn.exists:
                    next_btn.click()
                    time.sleep(5)
                    continue
                else:
                    break
        time_div3 = d(className="android.widget.ImageView", resourceId="com.kuaishou.nebula:id/neo_count_down_bg_image")
        time_div5 = d(className="android.widget.ImageView", resourceId="com.kuaishou.nebula:id/pendant_bg")
        # com.kuaishou.nebula:id/kem_activity_task_pendant
        if time_div3.exists(timeout=3) or time_div5.exists(timeout=3):
            print("第三种情况，无法定位到倒计时时间...")
            time.sleep(70)
            close_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container", className="android.widget.FrameLayout")
            if close_btn.exists:
                d.click(close_btn.center()[0], close_btn.center()[1])
                time.sleep(3)
                exit_btn = d(className="android.widget.TextView", text="退出直播间")
                if exit_btn.exists:
                    d.click(exit_btn.center()[0], exit_btn.center()[1])
                    time.sleep(2)
                break
        time.sleep(5)
    print("做任务结束，循环退出")


def find_task_btn():
    try_count = 0
    while True:
        print("开始查找去完成按钮...")
        try:
            to_btn = d(className="android.widget.Button", textMatches="去签到|去完成|看广告|去观看")
            if to_btn.exists:
                for view in to_btn:
                    text_div = view.left(className="android.view.View", index=1).child(className="android.view.View", index=0)
                    task_name = None
                    if text_div.exists:
                        task_name = text_div.get_text()
                    if not task_name or "打开喜番" in task_name:
                        continue
                    print(f"点击按钮：{task_name}")
                    view.click()
                    time.sleep(2)
                    operate_photo_detail()
                    take_foca()
                    break
            else:
                try_count += 1
                if try_count > 3:
                    print("未找到可点击按钮，退出循环")
                    break
        except Exception as e:
            print(e)
            continue
        time.sleep(4)


# 福卡首页
def foca_main():
    task_btn = d(className="android.widget.Button", text="做任务领卡")
    if task_btn.exists:
        task_btn.click()
        time.sleep(5)
        close_dialog()
        find_task_btn()


# 发财树首页
def pachira_main():
    time.sleep(5)
    get_btn = d(className="android.view.View", text="得次数")
    if get_btn.exists:
        print("点击得次数按钮")
        get_btn.click()
        time.sleep(5)
        find_task_btn()


# 收下福卡
def take_foca():
    time.sleep(4)
    try_count = 2
    print("开始查找<开心收下>按钮...")
    while try_count > 0:
        image = d.screenshot(format='opencv')
        pt = find_button(image, "kuaishou/ks-take.png")
        print(f"查找<开心收下>按钮结果={pt}")
        if pt:
            d.click(int(pt[0]) + 100, int(pt[1]) + 50)
            time.sleep(5)
            break
        try_count -= 1
        print(f"查找<开心收下>按钮，重试次数{2 - try_count}...")
        time.sleep(5)


# 点击摇金币
def waffle_coin():
    while True:
        coin_btn = d(className="android.widget.Button", resourceId="PRIMARY_BTN")
        if coin_btn.exists:
            print("点击摇金币按钮")
            coin_btn.click()
            time.sleep(2)
            try_count = 3
            while try_count >= 0:
                print("进入点击摇金币结果循环...")
                receive_btn = d(className="android.widget.Button", text="开心收下")
                continue_btn = d(className="android.widget.Button", text="继续摇")
                look_btn = d(className="android.widget.Button", text="去观看")
                if receive_btn.exists:
                    print("点击开心收下")
                    receive_btn.click()
                    time.sleep(3)
                    break
                elif continue_btn.exists:
                    print("点击继续摇")
                    continue_btn.click()
                    time.sleep(3)
                elif look_btn.exists:
                    print("点击去观看")
                    look_btn.click()
                    time.sleep(3)
                    operate_photo_detail()
                else:
                    pt = find_button(d.screenshot(format='opencv'), "./kuaishou/ks-close.png")
                    if pt:
                        print("点击关闭")
                        d.click(int(pt[0]) + 10, int(pt[1]) + 10)
                        time.sleep(2)
                        break
                try_count -= 1
                time.sleep(3)


print("查找去赚钱按钮...")
earn_btn = d(resourceId="android:id/text1", text="去赚钱")
if not earn_btn.exists:
    raise Exception("找不到赚钱按钮")
earn_btn.click()
print("进入去赚钱板块")
time.sleep(10)
ctx.wait_stable()
close_dialog()
while True:
    print("查找首页任务...")
    foca_btn = d(className="android.view.View", textContains="集福卡")
    if foca_btn.exists:
        print("进入集福卡页面")
        d.click(foca_btn.center()[0], foca_btn.center()[1])
        time.sleep(5)
        close_dialog()
        pachira_btn = d(className="android.widget.Button", text="发财树")
        if pachira_btn.exists:
            print("进入发财树页面")
            pachira_btn.click()
            time.sleep(5)
            close_dialog()
            # waffle_coin()
            pachira_main()
        foca_main()
    time.sleep(5)
# yao_btn = d(className="android.view.View", textContains="摇红包")
# if yao_btn.exists:
#     d.click(yao_btn.center()[0], yao_btn.center()[1])
#     time.sleep(8)
#     close_dialog()
# waffle_coin()
# fu_btn = d(className="android.widget.Button", text="集福卡")
# if fu_btn.exists:
#     fu_btn.click()
#     print("点击集福卡")
#     time.sleep(8)
#     close_dialog()
#     foca_main()
