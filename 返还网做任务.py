import time

import uiautomator2 as u2

d = u2.connect()
d.app_start("com.fanhuan", stop=True)
time.sleep(5)

title_list = d(resourceId="com.fanhuan:id/tvTitle", className="android.widget.TextView")
print(title_list)
