# 1. 导入依赖
from bs4 import BeautifulSoup  # 解析HTML
from app.crawlers.utils.request_utils import safe_request  # 导入安全请求工具
from app.db.models import PetDisease  # 数据库模型（用于存储数据）
from sqlalchemy.orm import Session  # 数据库会话类型


# 2. 核心爬虫函数
def crawl_pet_medical_data(url: str, db: Session):
    # - `url: str`：目标爬取的URL（由api.py传入）
    # - `db: Session`：数据库会话（用于操作数据库）

    # 2.1 临时调试打印（确认函数被调用）
    print(f"===== 爬虫函数已调用 {url}=====")

    # 2.2 日志记录（追踪流程）
    import logging
    logging.info(f"--------开始爬取URL：{url}=====")

    # 2.3 发送请求→获取页面HTML
    response = safe_request(url)  # 调用工具层的`safe_request`，获取页面响应
    soup = BeautifulSoup(response.text, "html.parser")  # 解析HTML为结构化对象

    # 2.4 提取数据列表（以豆瓣电影Top250为例）
    movie_items = soup.select(".grid_view li")  # 用CSS选择器提取所有电影条目
    logging.info(f"解析页面完成，共找到 {len(movie_items)} 条数据")

    # 2.5 遍历条目→提取详情→存储到数据库
    for idx, item in enumerate(movie_items):  # `enumerate`同时获取“索引”和“元素”
        try:
            # 提取电影标题
            title = item.select_one(".title").text.strip()
            # 提取电影简介
            intro_elem = item.select_one(".quote span")
            intro = intro_elem.text.strip() if intro_elem else "暂无简介"
            # 提取电影评分（可选）
            rating = item.select_one(".rating_num").text.strip()

            # 记录单条数据提取日志
            logging.info(f"[第{idx+1}条数据] 提取成功：{title}（评分{rating}）- {intro}")

            # 创建数据库记录对象（复用`PetDisease`模型，实际项目建议新建专用模型）
            db_movie = PetDisease(
                name=title,       # 电影标题存入`name`字段
                symptoms=intro,   # 电影简介存入`symptoms`字段（字段复用，临时方案）
                source_url=url    # 记录数据来源URL
            )

            # 将对象添加到数据库会话（暂存内存）
            db.add(db_movie)

        except Exception as e:
            # 捕获单条数据的异常，不中断整体流程
            logging.error(f"解析第{idx+1}条数据失败：{str(e)}")
            db.rollback()  # 回滚当前会话的错误操作

    # 2.6 提交所有数据到数据库（真正写入）
    db.commit()

    # 2.7 返回爬取数量（给api.py做响应）
    return len(movie_items)