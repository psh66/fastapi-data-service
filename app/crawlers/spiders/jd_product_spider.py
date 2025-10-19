from app.crawlers.utils.request_utils import safe_request
from app.crawlers.configs.jd_product import JD_PRODUCT_CONFIG
from app.crawlers.parsers import parse_data
from app.data_cleaning.pipelines import clean_data, CLEAN_PIPELINES
from app.db.models import Product
from bs4 import BeautifulSoup
from app.crawlers.utils.storage_utils import save_data
from app.db.session import get_db


def crawl_jd_products(url: str, db):
    # 1. 请求页面
    response = safe_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 2. 动态解析（用京东配置）
    raw_data_list = parse_data(soup, JD_PRODUCT_CONFIG)

    # 3. 数据清洗（用商品相关的清洗规则）
    cleaned_data_list = [
        clean_data(data, CLEAN_PIPELINES)
        for data in raw_data_list
    ]

    # 4. 存储到数据库（用Product模型）
    save_data(cleaned_data_list, db, Product)

    return len(cleaned_data_list)