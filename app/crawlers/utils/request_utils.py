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

        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
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
            headers["Cookie"] = "_xsrf=DmNEuoU9INZYPu7lKqwx8DYNJ9fdnPEB; __zse_ck=004_g4Y=D4wDXL3/mA60nd=wnxlYvZNVAPKKDOZPWcZkTjhaV=2VW1fAJiZxya3Dv1m7evdE/X9Cwm1wQkYetkVLauuMALHMzVIUD1g52yCOrytqYGHUpw8=NlZcbRsiqm43-6KbeZCwNkxVrbKUlcc1nFZhZ+mp0ZPomyu0bhYmM2MT6EBITz6wHJRJasHo6pkMGkPCmb0znOeg+TzQRteGj8htIJ90f9g7xDEehtUhw7C1p3IWNCA9PYJtyEMQZfleS; _zap=d76442d2-db72-4cad-a91a-40dbc13de53a; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1760931188; HMACCOUNT=A73F9F4F81489487; d_c0=fQfUVw7_PxuPTnIBvcQG4_xW-8odT2j4AxA=|1760931187; captcha_session_v2=2|1:0|10:1760931187|18:captcha_session_v2|88:Tys0eHlUYjdMejFadmVUVFY0VFN5ajIxeFVMWFlJMXhkdHo3czNBQ2N0UHZMbWw5Q29aWHdTSWVoYUhUMm9BcA==|cc46284e3704f3559d9e96137950485ee7cf05690418c27068def60502017dab; SESSIONID=MdfvLv42SHkmTT7p8Ir998LvUy4mDlzqdmylLzKYdUO; JOID=UlsSBUifyF-KIbR0Ij3MDE4rTUs-0ag4-W7BRBHPgzDmcONAVuxgruQhs3EmAg2eGRFQzlrq-YQPAnfcRDKrJWU=; osd=VFwSA0mZz1-MILJzIjvNCkkrS0o41qg--GjGRBfOhTfmduJGUexmr-Ims3cnBAqeHxBWyVrs-IIIAnHdQjWrI2Q=; __snaker__id=clr1V4LmC2wZHvPH; DATE=1760931188173; cmci9xde=U2FsdGVkX1+bvJWgNeX5RfMNZmHTGSyiRyJ706or9YpJZVTxgqGQHeeKucKcVstnBBpfeSu7vc3syONf+DL+Nw==; pmck9xge=U2FsdGVkX1+R9gyiOgNwKPxgXWIAaYG1gKc9cEWQNVk=; assva6=U2FsdGVkX19L6KoyWPUwY6c4m2UcBfojTohhi1V9McA=; assva5=U2FsdGVkX19VzkdYyQuPUpbaRuGM4drHGuV16LfY0fyNC3jSOZcAs64AXpk8pJ+DjebYM/2Arw6rtafTBvUBkA==; crystal=U2FsdGVkX1+Sw0yLN7AUNHsGJQkIJdIJ3xBeRUy9lEGOVL5PxP3j5jx72JZYyXIQtXlylQIIymIFo/9Xn2vaSMcRUYxIJzGcjDx63bvs3KJ0gT+BHaJqCkJ8bt1BIBAs4nE/x1dNX/9UWyMlBjskTHPiFG9x21ywGFmohSyMKiZd/sS58nHQ5L6Vgf16Vxi6L/dy8pfBnYxCWeakWiikxBDQXPgr70TBBo1MFbyi1zSlPuyBM/vKXjUFL4AxRB0k; gdxidpyhxdE=L9qJf67dRK5bSkoastfOllm6LXKzvBg8M6HvNn7BYsdw%5CxtTaBVpd7bKk1uuZpwin6%2FaAxDOtPEc92A78xVHJRz2Rx5WNxZ5qOi%2FNdW05PuB1G6iob4OVWpJftfG5aZu3XJi2lIK5GJJE2NTf7dJ4OOTzsPE6xqkmftVnq%2FNaTuIQOUL%3A1760932088515; vmce9xdq=U2FsdGVkX1+l5PzypxavziR2LxxIVMffVDKhmS98MEXPSnI6CBrFHKlgT7cfIKVjqvOYmAh4Tks0rU8LO2OD9l3paPJWlAv5lO8RVdxm1ov/0KG1VT1mNopqX1C9KgbO4HOrEECt0XhaV3xMwb/1CgU3IK6XAN1hRJmKxyy5SBQ=; captcha_ticket_v2=2|1:0|10:1760931200|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfVTJKUm1ITFppTzU2QXJLM1hIdWFjQ2NBUDBZWWoxam5SUVZUaUtCaFN1TypHY1FmVGpFenF1aTl6ZmlOalY0VkRyVWIzSXZCNXFHWEZDU19MOGY0V1hyeUNZSG16QmNRamppMUhoSVlWVTQwY1BsaENoKlZLZTNfeWJaeThVOTJGdWNsWjQ5Ll9ma0JuUEJhZjBXTjZLVEQyMkNVTDVwejRBSWIxSHkzRDZTamNkNCpkZzNGbkNVZWFXeXptOHg0T0txY3JfSWtJb1NvSlp1RWZEaldtZWVpcVdMXzVWX1NfZEpOQXJvT3pHbGhmUDBQNXhDbWhBUExfSW5sS1hEMnZvTklUXzhDWEFSbmcqUXZicGZ3ek90cFhJSVlCeVptSipSeGZ0TXlDQnRhQkhXT3FySlE2cVNNa1MyZDk4WHR1T3ZIMFRwbVBMbUpTNmhJMGZyRW9WTW1lSWloZVNORGlKa3V1UGVScHBfUmpRUk5RTHRHOG5BaGdNdHdTU2wxMWpnM1JKT0dGSWoqT0lyeVh4aWQyOHFkXzVLVSpMNWoubWdGT04qc1l1YjQ5RF9xMDM4MUE4c3NuS3FSc3J5SzhwY2dzQ3RybklVcC5pa0pBV1A2SExRTUt4UnBlcVhTa2tJOWFkSk9KYUdGR19iYXdGUmZPbmdURVk5akhOUnB6VE85bmc3N192X2lfMSJ9|99acd991dfa486e8d64a986c2cedd9f1764f3d14f3bf42c753f57af7da797684; z_c0=2|1:0|10:1760931231|4:z_c0|92:Mi4xSDBhdldnQUFBQUI5QjlSWER2OF9HeVlBQUFCZ0FsVk5uX3ZpYVFBd0cxVTYwYTZsM2FCTWJYazZGMmZ4S0pjRGtn|93c44182acc2341269bf1bcea7ea36f3b2546b6ba2fe686bea5f5d16d22bfcd8; q_c1=14800022a0e041ed82ba157466ca2603|1760931231000|1760931231000; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1760931253; BEC=92a0fca0e2e4d1109c446d0a990ad863"
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
            time.sleep(random.uniform(5, 10))

            # 3.8 返回响应对象（包含页面HTML等数据）
            return response

        except Exception as e:
            # 3.9 捕获异常，记录错误日志，休眠后重试
            logging.error(f"[第{i+1}次请求] 失败：{str(e)}")
            time.sleep(5)  # 失败后休眠5秒，避免频繁请求

    # 3.10 所有重试失败，抛出最终异常
    raise Exception(f"请求{url}失败，已重试{retry}次")