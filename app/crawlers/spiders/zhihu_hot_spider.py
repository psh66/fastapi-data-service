from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
# 导入清洗配置和函数
from app.data_cleaning.configs.zhihu_clean_rules import ZHIHU_CLEAN_RULES
from app.data_cleaning.pipelines import clean_zhihu_hot_list
# 其他原有导入
from app.crawlers.utils.request_utils import safe_request
from app.crawlers.parsers import parse_data
from app.crawlers.utils.storage_utils import save_data
from app.crawlers.configs.zhihu_hot import ZHIHU_HOT_CONFIG
from app.db.models import ZhihuHot


def crawl_zhihu_hot(url: str, db: Session):
    # 1. 发送请求并解析
    response = safe_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 2. 提取原始数据（假设parse_data返回列表，每个元素为单条热榜原始数据）
    raw_data_list = parse_data(soup, ZHIHU_HOT_CONFIG)
    print(f"原始数据共 {len(raw_data_list)} 条：", raw_data_list[:2])  # 打印前2条调试

    # 3. 数据清洗（核心步骤）
    cleaned_data_list = clean_zhihu_hot_list(raw_data_list, ZHIHU_CLEAN_RULES)
    print(f"清洗后数据共 {len(cleaned_data_list)} 条：", cleaned_data_list[:2])  # 打印前2条调试

    # 4. 过滤无效数据（可选：移除关键字段缺失的条目）
    valid_data_list = [item for item in cleaned_data_list if all(key in item for key in ZHIHU_CLEAN_RULES.keys())]
    print(f"有效数据共 {len(valid_data_list)} 条")

    # 5. 存储到数据库
    save_data(valid_data_list, db, ZhihuHot)
    return len(valid_data_list)


# # 测试入口（包含建表逻辑）
# if __name__ == "__main__":
#     from app.db.session import get_db, engine, Base
#     from app.db.models import ZhihuHot
#
#     # 确保表存在
#     Base.metadata.create_all(bind=engine)
#     print("zhihu_hot 表已创建（若不存在）")
#
#     # 执行爬取
#     db = next(get_db())
#     test_url = "https://www.zhihu.com/hot"
#     count = crawl_zhihu_hot(test_url, db)
#     print(f"成功爬取并存储 {count} 条知乎热榜数据")

if __name__ == "__main__":
    from app.db.session import get_db, engine, Base
    from app.db.models import ZhihuHot
    import datetime

    Base.metadata.create_all(bind=engine)  # 确保表存在
    db = next(get_db())  # 获取数据库会话

    # 执行爬取和存储
    test_url = "https://www.zhihu.com/hot"
    count = crawl_zhihu_hot(test_url, db)
    print(f"成功爬取 {count} 条数据")

    # 存储后立即查询，验证是否真的存入
    latest = db.query(ZhihuHot).order_by(ZhihuHot.id.desc()).first()
    if latest:
        print("代码中查询到的最新数据：")
        print(f"id: {latest.id}, rank: {latest.rank}, title: {latest.title}")
    else:
        print("代码中未查询到任何数据，存储失败！")