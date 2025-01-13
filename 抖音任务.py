import time

import uiautomator2 as u2

d = u2.connect()
d.app_start("com.ss.android.ugc.aweme.lite")
# time.sleep(5)
# earn_btn = d(resourceId="com.ss.android.ugc.aweme.lite:id/d3w")
# if earn_btn.exists:
#     earn_btn.click()
#     time.sleep(5)
# else:
#     raise Exception("找不到赚钱按钮")
d(text="")
