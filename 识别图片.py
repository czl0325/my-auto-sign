import cv2
import numpy as np

# 读取截图和模板图像
screenshot = cv2.imread('screenshot.png')
template = cv2.imread('kuaishou/ks-take.png')

# 转换为灰度图像
screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# 获取模板图像的宽度和高度
w, h = template_gray.shape[::-1]

# 使用模板匹配
res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
# 绘制矩形框标记按钮位置
for pt in zip(*loc[::-1]):
    x, y = pt
    print(f"找到按钮的位置: 左上角坐标 (x={x}, y={y})，宽度 (w={w})，高度 (h={h})")
    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

# # 显示结果图像
# cv2.imshow('Detected Button', screenshot)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
