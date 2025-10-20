from bs4 import BeautifulSoup  # 用于解析HTML页面，提取数据（如热榜标题、排名等）
from sqlalchemy.orm import Session  # 数据库会话类型注解（指定函数参数`db`的类型）
# 导入清洗配置和函数（知乎热榜专用）
from app.data_cleaning.configs.zhihu_clean_rules import ZHIHU_CLEAN_RULES  # 清洗规则（定义每个字段如何处理）
from app.data_cleaning.pipelines import clean_zhihu_hot_list  # 批量清洗知乎热榜数据的函数
# 其他工具导入
from app.crawlers.utils.request_utils import safe_request  # 安全请求工具（处理超时、重试、异常）
from app.crawlers.parsers import parse_data  # 通用数据解析函数（根据配置提取原始数据）
from app.crawlers.utils.storage_utils import save_data  # 通用数据存储函数（批量插入数据库）
from app.crawlers.configs.zhihu_hot import ZHIHU_HOT_CONFIG  # 知乎热榜解析配置（定义如何从HTML提取字段）
from app.db.models import ZhihuHot  # 知乎热榜数据库模型（对应表结构


def crawl_zhihu_hot(url: str, db: Session):  # 定义函数：接收爬取URL和数据库会话（db用于操作数据库）
    # 步骤1：发送请求并解析HTML
    response = safe_request(url)  # 调用安全请求函数：发送GET请求，自动处理超时、500错误等，返回响应对象
    soup = BeautifulSoup(response.text, "html.parser")  # 用BeautifulSoup解析响应文本为HTML对象（类似网页DOM树）

    # 步骤2：提取原始数据（从HTML中提取未处理的原始字段）
    raw_data_list = parse_data(soup, ZHIHU_HOT_CONFIG)  # 根据ZHIHU_HOT_CONFIG规则提取数据
    # 打印前2条原始数据（调试用，确认提取的字段是否正确，如rank、title等是否存在）
    print(f"原始数据共 {len(raw_data_list)} 条：", raw_data_list[:2])

    # 步骤3：数据清洗（核心步骤，将原始数据标准化）
    cleaned_data_list = clean_zhihu_hot_list(raw_data_list, ZHIHU_CLEAN_RULES)  # 用规则批量清洗数据
    # 打印前2条清洗后数据（调试用，确认格式是否正确，如rank是否转为整数、标题是否去空格）
    print(f"清洗后数据共 {len(cleaned_data_list)} 条：", cleaned_data_list[:2])

    # 步骤4：过滤无效数据（确保所有关键字段都存在，避免存储时因缺失字段报错）
    # 检查每条数据是否包含ZHIHU_CLEAN_RULES中定义的所有字段（rank、title、hot_value、url）
    valid_data_list = [item for item in cleaned_data_list if all(key in item for key in ZHIHU_CLEAN_RULES.keys())]
    print(f"有效数据共 {len(valid_data_list)} 条")  # 打印过滤后的有效数据量

    # 步骤5：存储有效数据到数据库
    save_data(valid_data_list, db, ZhihuHot)  # 调用存储函数，将数据插入ZhihuHot对应的表
    return len(valid_data_list)  # 返回成功爬取并存储的数量


if __name__ == "__main__":  # 当直接运行本脚本时（非被其他模块导入），执行以下代码
    # 导入数据库相关工具和模型
    from app.db.session import get_db, engine, Base  # get_db：获取数据库会话；engine：数据库连接引擎；Base：模型基类
    from app.db.models import ZhihuHot  # 显式导入模型（确保建表时Base能识别它）
    import datetime  # 时间处理模块（模型中crawl_time字段用）

    Base.metadata.create_all(bind=engine)  # 关键：根据Base中注册的模型（如ZhihuHot）创建数据库表（若不存在）
    db = next(get_db())  # 从会话生成器中获取一个数据库会话（类似“数据库连接”，用于后续操作）

    # 执行爬取和存储
    test_url = "https://www.zhihu.com/hot"  # 知乎热榜首页URL
    count = crawl_zhihu_hot(test_url, db)  # 调用爬虫函数，传入URL和会话
    print(f"成功爬取 {count} 条数据")  # 打印爬取结果

    # 存储后立即查询，验证数据是否真的存入数据库
    latest = db.query(ZhihuHot).order_by(ZhihuHot.id.desc()).first()  # 查询最新一条数据（按id倒序取第一条）
    if latest:  # 若查询到数据，打印详情
        print("代码中查询到的最新数据：")
        print(f"id: {latest.id}, rank: {latest.rank}, title: {latest.title}")
    else:  # 若未查询到，提示存储失败
        print("代码中未查询到任何数据，存储失败！")