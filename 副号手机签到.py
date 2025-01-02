import uiautomator2 as u2
import time

d = u2.connect()
d.shell("adb kill-server && adb start-server")
time.sleep(5)

d.watcher.when(xpath='//*[@resource-id="com.pingan.lifeinsurance:id/aa"]').click()
d.watcher.when(xpath='//*[@resource-id="com.pingan.lifeinsurance:id/bse"]').click()
d.watcher.when(xpath='//*[@resource-id="com.suning.mobile.epa:id/sale_info_close"]').click()
d.watcher.when(xpath='//*[@resource-id="com.baidu.netdisk:id/iv_close"]').click()
d.watcher.start()

# 新浪微博签到
d.app_start("com.sina.weibo", stop=True)
time.sleep(5)
me_btn = d(className="android.widget.FrameLayout", description="我")
if me_btn.exists:
    me_btn.click()
    sign_btn = d(resourceId="com.sina.weibo:id/tv_content", text="签到")
    if sign_btn.exists:
        d.click(sign_btn.center()[0], sign_btn.center()[1])
        time.sleep(2)
d.app_stop("com.sina.weibo")
# 平安金管家
d.app_start("com.pingan.lifeinsurance", stop=True)
time.sleep(5)
sign_btn = d(resourceId="com.pingan.lifeinsurance:id/h8v", text="签到")
if sign_btn.exists:
    d.click(sign_btn.center()[0], sign_btn.center()[1])
    time.sleep(5)
d.app_stop("com.pingan.lifeinsurance")
# 喜马拉雅
d.app_start("com.ximalaya.ting.android", stop=True)
me_btn = d(resourceId="com.ximalaya.ting.android:id/tab_myspace_and_listen", text="我的")
if me_btn.exists:
    me_btn.click()
    sign_btn = d(resourceId="com.ximalaya.ting.android:id/main_iv_entrance")
    if sign_btn.exists:
        d.click(sign_btn.center()[0], sign_btn.center()[1])
        time.sleep(5)
d.app_stop("com.ximalaya.ting.android")
# 星图金融
d.app_start("com.suning.mobile.epa", stop=True)
time.sleep(5)
sign_btn = d(resourceId="com.suning.mobile.epa:id/item_text", className="android.widget.TextView", textContains="签到")
if sign_btn.exists:
    d.click(sign_btn.center()[0], sign_btn.center()[1])
    time.sleep(2)
    sign_btn = d(resourceId="signBtnRef", className="android.view.View")
    if sign_btn.exists:
        d.click(sign_btn.center()[0], sign_btn.center()[1])
        time.sleep(5)
d.app_stop("com.suning.mobile.epa")
# 百度网盘
d.app_start("com.baidu.netdisk", stop=True)
time.sleep(5)
me_btn = d(className="android.widget.LinearLayout", resourceId="com.baidu.netdisk:id/rb_about_me")
if me_btn.exists:
    d.click(me_btn.center()[0], me_btn.center()[1])
    time.sleep(5)
    sign_btn = d(className="android.widget.TextView", resourceId="com.baidu.netdisk:id/tv_subtitle", textContains="领金币")
    if sign_btn.exists:
        d.click(sign_btn.center()[0], sign_btn.center()[1])
        time.sleep(5)
d.app_stop("com.baidu.netdisk")
# 天翼云盘
d.app_start("com.cn21.ecloud", stop=True)

d.watcher.remove()
