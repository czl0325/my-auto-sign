import re
import cv2
import numpy as np


def get_current_app(d):
    info = d.shell("dumpsys window | grep mCurrentFocus").output
    match = re.search(r'mCurrentFocus=Window\{.*? u0 (.*?)/(.*?)\}', info)
    if match:
        package_name = match.group(1)
        activity_name = match.group(2)
        return package_name, activity_name
    return None, None


def find_button(image, btn_path):
    template = cv2.imread(btn_path)
    screenshot_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]
    res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return pt
    return None


def countdown_to_seconds(countdown_str):
    """
    将倒计时字符串（如 "11:35"）转换为总秒数
    """
    minutes, seconds = map(int, countdown_str.split(":"))
    return minutes * 60 + seconds