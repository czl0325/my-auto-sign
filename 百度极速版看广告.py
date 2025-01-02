import time
import uiautomator2 as u2

d = u2.connect()
d.shell("adb kill-server && adb start-server")
time.sleep(5)
d.app_stop("com.baidu.searchbox.lite")
time.sleep(2)
d.app_start("com.baidu.searchbox.lite", stop=True)
time.sleep(2)
me_btn = d.xpath('//android.widget.TextView[@text="我的"]')
print(me_btn)
if me_btn.exists:
    d.click(me_btn.center()[0], me_btn.center()[1] - 10)
    time.sleep(2)
sign_btn = d(resourceId="com.baidu.searchbox.lite:id/vu")
if sign_btn.exists:
    sign_btn.click()
    time.sleep(2)
web_view = d(className="com.baidu.webkit.sdk.WebView")
if web_view.exists:
    print(web_view)