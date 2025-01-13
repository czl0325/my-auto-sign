import uiautomator2 as u2
import time

d = u2.connect()
d.app_start("com.kuaishou.nebula", stop=True)
ctx = d.watch_context()
ctx.when(xpath='//*[@resource-id="com.kuaishou.nebula:id/popup_view"]//*[@resource-id="com.kuaishou.nebula:id/close_btn"]').click()
ctx.wait_stable()


def back_to_main():
    while True:
        home_view = d(className="android.view.View", text="任务中心")
        if home_view.exists:
            break
        d.press("back")
        time.sleep(0.5)


def operate_advertisement_task():
    while True:
        time_view = d(resourceId="com.kuaishou.nebula.commercial_neo:id/video_countdown")
        if time_view.exists:
            time_text = time_view.get_text()
            if "已成功领取" in time_text:
                time_view.click()
                time.sleep(3)
                next_btn = d(resourceId="com.kuaishou.nebula.commercial_neo:id/again_medium_icon_dialog_ensure_text", text="领取奖励")
                if next_btn.exists:
                    next_btn.click()
                    time.sleep(5)
                    continue
            else:
                time.sleep(5)
        else:
            break


def operate_clock_task():
    sign_btn = d(className="android.widget.Button", text="去签到")
    if sign_btn.exists:
        sign_btn.click()
        time.sleep(5)
        see_btn = d(className="android.widget.Button", text="看视频赚金币")
        if see_btn.exists:
            see_btn.click()
            operate_advertisement_task()


def operate_video_task():
    start_time = time.time()
    while True:
        if time.time() - start_time > 60 * 50:
            break
        time.sleep(20)
        d.swipe_ext(u2.Direction.FORWARD)


print("查找去赚钱按钮...")
earn_btn = d(resourceId="android:id/text1", text="去赚钱")
if not earn_btn.exists:
    raise Exception("找不到赚钱按钮")
earn_btn.click()
time.sleep(5)
while True:
    click_btn = d(className="android.widget.Button", textContains="点可领")
    if click_btn.exists:
        click_btn.click()
        time.sleep(4)
        advert_btn = d(className="android.widget.Button", textContains="去看广告得最高")
        if advert_btn.exists:
            advert_btn.click()
            time.sleep(2)
            operate_advertisement_task()
        continue
    to_btn = d(className="android.view.View", textMatches="立即签到|去观看|去打卡|去领取")
    if to_btn.exists:
        text_div = to_btn.sibling(className="android.view.View").child(className="android.view.View")
        if text_div.exists:
            if len(text_div) == 2:
                title = text_div[0].get_text()
                subtitle = text_div[1].get_text()
                if title == "看视频赚金币":
                    continue
        # to_btn.click()
        # time.sleep(5)
    else:
        break
    # advert_view = d(className="android.view.View", resourceId="com.kuaishou.nebula.commercial_neo:id/award_video_player_textureview")
    # if advert_view.exists:
    #     print("进行广告任务")
    #     operate_advertisement_task()
    #     continue
    # clock_view = d(className="android.view.View", textContains="完成365天打卡任务")
    # if clock_view.exists:
    #     print("进行签到任务")
    #     operate_clock_task()
    #     continue
    # video_view = d(className="android.widget.FrameLayout", resourceId="com.kuaishou.nebula:id/texture_view_frame")
    # if video_view.exists:
    #     print("进行看视频任务")
    #     operate_video_task()
    #     continue
ctx.close()
d.shell("settings put system accelerometer_rotation 0")
print("关闭手机自动旋转")
