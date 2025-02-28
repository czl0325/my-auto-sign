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
ctx.when("打开").click()
ctx.start()
time.sleep(5)


print("查找去赚钱按钮...")
earn_btn = d(resourceId="android:id/text1", text="去赚钱")
if not earn_btn.exists:
    raise Exception("找不到赚钱按钮")
earn_btn.click()
print("进入去赚钱板块")