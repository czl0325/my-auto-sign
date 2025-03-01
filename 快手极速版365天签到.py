import uiautomator2 as u2
import time
from utils import find_button, countdown_to_seconds
from uiautomator2 import Direction

d = u2.connect()
screen_width, screen_height = d.window_size()
d.app_start("com.kuaishou.nebula", stop=True, use_monkey=True)
ctx = d.watch_context()
ctx.start()
time.sleep(5)


def check_popup():
    phone_popup =  d(className="android.widget.Image", text="huge_sign_marketing_popup")
    if phone_popup.exists:
        pt = find_button(d.screenshot(format='opencv'), "./kuaishou/ks-close.png")
        if pt:
            d.click(int(pt[0]) + 10, int(pt[1]) + 10)
            time.sleep(2)


def task_loop():
    last_time = None
    while True:
        finish_view = d(resourceId="com.kuaishou.nebula:id/kem_activity_task_pendant", className="android.widget.FrameLayout")
        if finish_view.exists:
            print("当前已完成任务。")
            d.press("back")
            break
        countdown_view = d(resourceId="com.kuaishou.nebula:id/pendant_task_status", className="android.widget.TextView")
        if countdown_view.exists:
            countdown_text = countdown_view.get_text()
            print(countdown_text)
            countdown_time = countdown_text.replace("倒计时 ", "")
            if last_time:
                seconds1 = countdown_to_seconds(last_time)
                seconds2 = countdown_to_seconds(countdown_time)
                if abs(seconds1 - seconds2) <= 5:
                    d.swipe_ext(Direction.FORWARD)
            last_time = countdown_time
        time.sleep(10)


check_popup()
print("查找去赚钱按钮...")
earn_btn = d(resourceId="android:id/text1", text="去赚钱")
if not earn_btn.exists:
    raise Exception("找不到赚钱按钮")
earn_btn.click()
print("进入去赚钱板块")
time.sleep(8)
clock_in_view = d(className="android.view.View", textContains="拿好礼")
if clock_in_view.exists:
    print("点击拿好礼")
    d.click(clock_in_view.center()[0], clock_in_view.center()[1])
    time.sleep(5)
else:
    raise Exception("找不到拿好礼按钮，请重启程序")
print("当前位于打开页面")
sign_btn = d(className="android.view.View", text="去签到")
if sign_btn.exists:
    print("点击去签到")
    d.click(sign_btn.center()[0], sign_btn.center()[1])
    time.sleep(5)
look_btn = d(className="android.widget.Button", text="去观看")
if look_btn.exists:
    current_task = None
    for btn in look_btn:
        text_div = btn.left(className="android.view.View", index=1).child(className="android.view.View", index=0)
        if text_div.exists:
            current_task = text_div.get_text()
            print("当前任务是:", current_task)
        btn.click()
        time.sleep(4)
        task_loop()