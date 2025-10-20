from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
# 导入通用模块
from app.crawlers.utils.request_utils import safe_request
from app.crawlers.parsers import parse_data
from app.crawlers.utils.storage_utils import save_data
# 导入知乎配置和清洗规则
from app.crawlers.configs.zhihu_hot import ZHIHU_HOT_CONFIG
from app.data_cleaning.pipelines import clean_data, CLEAN_PIPELINES
# 导入数据库模型（需提前定义）
from app.db.models import ZhihuHot


def crawl_zhihu_hot(url: str, db: Session):
    response = safe_request(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print("页面解析内容：", soup.select_one(".HotItem").prettify())  # 打印完整条目HTML

    raw_data_list = parse_data(soup, ZHIHU_HOT_CONFIG)
    print("原始数据：", raw_data_list)

    cleaned_data_list = [clean_data(data, CLEAN_PIPELINES) for data in raw_data_list]
    print("清洗后数据：", cleaned_data_list)

    save_data(cleaned_data_list, db, ZhihuHot)
    return len(cleaned_data_list)


# 测试入口（单独运行脚本时使用）
if __name__ == "__main__":
    from app.db.session import get_db, engine, Base  # 导入 Base 和引擎
    from app.db.models import ZhihuHot  # 显式导入模型（关键！）

    # 先创建表（如果不存在）
    Base.metadata.create_all(bind=engine)
    print("zhihu_hot 表已创建（若之前不存在）")

    # 再爬取数据
    db = next(get_db())
    test_url = "https://www.zhihu.com/hot"
    count = crawl_zhihu_hot(test_url, db)
    print(f"成功爬取 {count} 条知乎热榜数据")