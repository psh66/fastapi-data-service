# 1. 导入依赖
import requests  # 发送HTTP请求
import time  # 控制时间间隔
import random  # 生成随机数
from fake_useragent import UserAgent  # 生成随机浏览器标识（需安装：`pip install fake-useragent`）


# 2. 生成“随机请求头”（反爬核心）
def get_random_headers():
    """模拟真实浏览器的请求头，避免被网站识别为爬虫"""
    ua = UserAgent()  # 初始化UA生成器
    return {
        "User-Agent": ua.random,  # 随机生成浏览器标识（如Chrome、Firefox等）
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # 声明可接收的内容类型
        "Referer": "https://www.baidu.com/"  # 模拟“从百度跳转”，降低反爬概率
    }


# 3. 安全请求函数（带重试、异常处理）
def safe_request(url, method="GET", retry=3, **kwargs):
    """处理“请求失败、超时、反爬”等问题，确保稳定获取页面"""
    import logging  # 导入日志模块（记录请求过程）
    for i in range(retry):  # 最多重试`retry`次（默认3次）
        try:
            # 3.1 记录“请求开始”日志
            logging.info(f"[第{i+1}次请求:{url}, 方法:{method}]")

            # 3.2 记录请求开始时间（用于计算耗时）
            start_time = time.time()

            # 3.3 获取随机请求头
            headers = get_random_headers()

            # 3.4 发送HTTP请求
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30, **kwargs)
            else:
                response = requests.post(url, headers=headers, timeout=30, **kwargs)

            # 3.5 校验请求是否成功（若状态码是4xx/5xx，抛出异常）
            response.raise_for_status()

            # 3.6 记录“请求成功”日志（含状态码、耗时）
            end_time = time.time()
            logging.info(f"[第{i+1}次请求]：{response.status_code}，耗时：{end_time - start_time:.2f}秒")

            # 3.7 随机休眠（模拟人类浏览间隔，避免高频请求被封）
            time.sleep(random.uniform(3, 5))

            # 3.8 返回响应对象（包含页面HTML等数据）
            return response

        except Exception as e:
            # 3.9 捕获异常，记录错误日志，休眠后重试
            logging.error(f"[第{i+1}次请求] 失败：{str(e)}")
            time.sleep(5)  # 失败后休眠5秒，避免频繁请求

    # 3.10 所有重试失败，抛出最终异常
    raise Exception(f"请求{url}失败，已重试{retry}次")