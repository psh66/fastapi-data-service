# app/crawlers/spiders/jd_product_spider.py
from bs4 import BeautifulSoup
# 导入安全请求工具
from app.crawlers.utils.request_utils import safe_request
# 导入通用解析函数
from app.crawlers.parsers import parse_data
# 导入通用存储函数
from app.crawlers.utils.storage_utils import save_data
# 导入京东商品配置
from app.crawlers.configs.jd_product import JD_PRODUCT_CONFIG
# 导入数据清洗逻辑
from app.data_cleaning.pipelines import clean_data, CLEAN_PIPELINES
# 导入数据库模型
from app.db.models import Product
from sqlalchemy.orm import Session


def crawl_jd_products(url: str, db: Session):
    # 1. 调用 request_utils.py 发送请求
    response = safe_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 2. 调用 parsers.py 动态解析（使用京东配置）
    raw_data_list = parse_data(soup, JD_PRODUCT_CONFIG)

    # 3. 调用 data_cleaning 模块清洗数据
    cleaned_data_list = [clean_data(data, CLEAN_PIPELINES) for data in raw_data_list]

    # 4. 调用 storage_utils.py 存储数据（使用Product模型）
    save_data(cleaned_data_list, db, Product)

    return len(cleaned_data_list)