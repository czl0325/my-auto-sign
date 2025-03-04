import uiautomator2 as u2
import time
from utils import find_button, countdown_to_seconds
from uiautomator2 import Direction
from enum import Enum


class VideoTask(Enum):
    LEFT_TOP = 1
    RIGHT_TOP = 2
    DURATION = 3

d = u2.connect()
screen_width, screen_height = d.window_size()
d.app_start("com.kuaishou.nebula", stop=True, use_monkey=True)
ctx = d.watch_context()
ctx.start()
time.sleep(5)


def check_popup():
    sign_dialog = d(className="android.widget.Button", text="立即签到")
    if sign_dialog.exists:
        print("点击立即签到")
        sign_dialog.click()
        time.sleep(5)
        look_dialog = d(className="android.widget.Button", textContains="看内容最高可得")
        if look_dialog.exists:
            look_dialog.click()
            task_loop()
            check_popup()
        return
    phone_popup = d(className="android.widget.Image", text="huge_sign_marketing_popup")
    if phone_popup.exists:
        pt = find_button(d.screenshot(format='opencv'), "./kuaishou/ks-close.png")
        if pt:
            d.click(int(pt[0]) + 10, int(pt[1]) + 10)
            time.sleep(2)
        return
    pt = find_button(d.screenshot(format='opencv'), "./kuaishou/ks-close.png")
    if pt:
        d.click(int(pt[0]) + 10, int(pt[1]) + 10)
        time.sleep(2)
    close_btn = d(resourceId="com.kuaishou.nebula:id/close_btn", className="android.widget.ImageView")
    if close_btn.exists:
        d.click(close_btn.center()[0], close_btn.center()[1])
        time.sleep(2)


def finish_task(video_type):
    close_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_audience_clearable_close_container", className="android.widget.FrameLayout")
    print(f"右上角关闭按钮是否存在:{close_btn.exists}")
    if close_btn.exists:
        d.click(close_btn.center()[0], close_btn.center()[1])
        time.sleep(3)
    back_btn = d(resourceId="com.kuaishou.nebula.live_audience_plugin:id/live_anchor_avatar_icon", className="android.widget.ImageView")
    if back_btn.exists:
        d.click(back_btn.center()[0], back_btn.center()[1])
        time.sleep(3)
    video_type = None


def to_earn():
    print("查找去赚钱按钮...")
    earn_btn = d(resourceId="android:id/text1", text="去赚钱")
    if not earn_btn.exists:
        raise Exception("找不到赚钱按钮")
    earn_btn.click()
    print("进入去赚钱板块")
    time.sleep(8)
    check_popup()


def task_loop():
    last_time = None
    video_type = None
    while True:
        countdown_view = d(resourceId="com.kuaishou.nebula:id/pendant_task_status", className="android.widget.TextView")
        if countdown_view.exists:
            video_type = VideoTask.DURATION
            try:
                countdown_text = countdown_view.get_text()
                print(countdown_text)
                if countdown_text == "领取奖励":
                    print("当前已完成任务。")
                    d.press("back")
                    break
                countdown_time = countdown_text.replace("倒计时 ", "")
                if last_time:
                    seconds1 = countdown_to_seconds(last_time)
                    seconds2 = countdown_to_seconds(countdown_time)
                    if abs(seconds1 - seconds2) <= 5:
                        print("倒计时停了，滑动进入下一个视频。。。")
                        d.swipe_ext(Direction.FORWARD)
                last_time = countdown_time
            except Exception as e:
                video_type = None
                to_earn()
        time_div1 = d(className="android.widget.TextView", resourceId="com.kuaishou.nebula:id/neo_count_down_text")
        if time_div1.exists:
            time_text = time_div1.get_text()
            print(f"属于右上角小图标时间类型,获取到的时间是:{time_text}")
            video_type = VideoTask.RIGHT_TOP
            if time_text == "已领取":
                finish_task(video_type)
        time_div2 = d(resourceId="com.kuaishou.nebula.commercial_neo:id/video_countdown", className="android.widget.TextView")
        if time_div2.exists:
            time_text = time_div2.get_text()
            print(f"属于左上角类型,获取到的时间是:{time_text}")
            video_type = VideoTask.LEFT_TOP
            if "成功领取" in time_text:
                d.click(time_div2.center()[0], time_div2.center()[1])
                time.sleep(5)
        award_btn = d(resourceId="com.kuaishou.nebula:id/again_dialog_ensure_text", text="领取奖励")
        if award_btn.exists:
            award_btn.click()
            time.sleep(5)
        # 退出直播间退出循环
        quit_btn = d(className="android.widget.TextView", text="退出直播间")
        if quit_btn.exists:
            d.click(quit_btn.center()[0], quit_btn.center()[1])
            time.sleep(5)
            break
        # 放弃奖励退出循环
        to_btn = d(resourceId="com.kuaishou.nebula:id/close_dialog_ensure_text", text="去完成任务")
        if to_btn.exists:
            waive_btn = d(resourceId="com.kuaishou.nebula.commercial_neo:id/award_video_close_dialog_abandon_button", text="放弃奖励")
            if waive_btn.exists:
                waive_btn.click()
                time.sleep(3)
                break
        time.sleep(10)


check_popup()
to_earn()
clock_in_view = d(className="android.view.View", textContains="拿好礼")
if clock_in_view.exists(timeout=10):
    print("点击拿好礼")
    d.click(clock_in_view.center()[0], clock_in_view.center()[1])
    time.sleep(5)
else:
    raise Exception("找不到拿好礼按钮，请重启程序")
print("当前位于365天签到领好礼页面")
sign_btn = d(className="android.widget.Button", text="去签到")
if sign_btn.exists:
    print("点击去签到")
    d.click(sign_btn.center()[0], sign_btn.center()[1])
    time.sleep(5)
while True:
    look_btn = d(className="android.widget.Button", text="去观看")
    if look_btn.exists:
        look_btn[0].click()
        time.sleep(5)
        task_loop()
    else:
        break
