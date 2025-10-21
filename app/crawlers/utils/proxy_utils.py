# app/crawlers/utils/proxy_utils.py
import requests
from random import choice
from datetime import datetime

PROXY_POOL = [
    "http://112.84.171.113:9999",
    "http://183.247.205.184:8080",
    # 可从免费代理网站补充更多代理
]
LAST_CHECK_TIME = None
VALID_PROXIES = []

def check_proxy(proxy):
    """验证代理是否有效（访问 GitHub 测试）"""
    try:
        resp = requests.get("https://github.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return resp.status_code == 200
    except:
        return False

def get_random_proxy():
    """从代理池获取一个随机有效代理（每小时验证一次）"""
    global LAST_CHECK_TIME, VALID_PROXIES
    now = datetime.now()
    if not LAST_CHECK_TIME or (now - LAST_CHECK_TIME).total_seconds() > 3600:
        VALID_PROXIES = [p for p in PROXY_POOL if check_proxy(p)]
        LAST_CHECK_TIME = now
    return choice(VALID_PROXIES) if VALID_PROXIES else None