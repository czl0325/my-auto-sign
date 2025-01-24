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
ctx.start()
time.sleep(5)


def operate_photo_detail():
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
        if time_div1.exists(timeout=3):
            time_text = time_div1.get_text()
            print(f"属于右上角小图标时间类型,获取到的时间是:{time_text}")
            if ":" in time_text:
                sleep_time = int(time_text.split(":")[1])
                time.sleep(sleep_time + 5)
                close_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container", className="android.widget.FrameLayout")
                if close_btn.exists:
                    d.click(close_btn.center()[0], close_btn.center()[1])
                    time.sleep(3)
                exit_btn = d(className="android.widget.TextView", text="退出")
                if exit_btn.exists:
                    d.click(exit_btn.center()[0], exit_btn.center()[1])
                    time.sleep(5)
                    next_btn = d(resourceId="com.kuaishou.nebula.commercial_neo:id/again_medium_icon_dialog_ensure_text", text="领取奖励")
                    if next_btn.exists:
                        next_btn.click()
                        time.sleep(5)
                        continue
                    else:
                        break
        time_div3 = d(className="android.widget.ImageView", resourceId="com.kuaishou.nebula:id/neo_count_down_bg_image")
        if time_div3.exists(timeout=3):
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


def foca_task():
    task_btn = d(className="android.widget.Button", text="做任务领卡")
    if task_btn.exists:
        task_btn.click()
        time.sleep(5)
        while True:
            try:
                to_btn = d(className="android.widget.Button", textMatches="去签到|去完成")
                if to_btn.exists:
                    for view in to_btn:
                        text_div = view.left(className="android.view.View").sibling(className="android.view.View", index=1).child(className="android.view.View", index=0)
                        task_name = None
                        if text_div.exists:
                            task_name = text_div.get_text()
                            print(f"点击按钮：{task_name}")
                        view.click()
                        time.sleep(2)
                        operate_photo_detail()
                        take_foca()
                        break
            except Exception as e:
                print(e)
                continue


def take_foca():
    time.sleep(4)
    while True:
        image = d.screenshot(format='opencv')
        pt = find_button(image, "slot1.png")
        print(f"查找按钮结果={pt}")
        if pt:
            d.click(int(pt[0]) + 100, int(pt[1]) + 50)
            time.sleep(5)
            break
        time.sleep(5)


print("查找去赚钱按钮...")
earn_btn = d(resourceId="android:id/text1", text="去赚钱")
if not earn_btn.exists:
    raise Exception("找不到赚钱按钮")
earn_btn.click()
print("进入去赚钱板块")
time.sleep(10)
ctx.wait_stable()

yao_btn = d(className="android.view.View", textContains="摇红包")
if yao_btn.exists:
    d.click(yao_btn.center()[0], yao_btn.center()[1])
    time.sleep(8)
fu_btn = d(className="android.widget.Button", text="集福卡")
if fu_btn.exists:
    fu_btn.click()
    print("点击集福卡")
    time.sleep(8)
    foca_task()
# while True:
#     current_info = d.app_current()
#     if current_info.get("activity") == "com.yxcorp.gifshow.detail.PhotoDetailActivity":
#         close_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container", className="android.widget.FrameLayout")
#         if close_btn.exists:
#             d.click(close_btn.center()[0], close_btn.center()[1])
#             time.sleep(4)
#     elif current_info.get("activity") == "com.yxcorp.gifshow.webview.KwaiYodaWebViewActivity":
#         break
