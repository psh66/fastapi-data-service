# 1. 导入依赖
from fastapi import APIRouter, Depends  # 用于定义路由和依赖注入
from sqlalchemy.orm import Session  # 数据库会话类型
from app.db.session import get_db  # 项目中定义的“获取数据库会话”函数
from app.crawlers.spiders.pet_medical_spider import crawl_pet_medical_data  # 核心爬虫函数

# 2. 创建路由组
router = APIRouter(prefix="/crawlers", tags=["爬虫"])  
# - `prefix="/crawlers"`：该路由下所有接口的URL前缀为 `/crawlers`
# - `tags=["爬虫"]`：在Swagger文档中归类为“爬虫”标签，方便接口管理


# 3. 定义POST接口：触发爬虫
@router.post("/crawl_pet_medical")
def trigger_pet_medical_crawler(url: str, db: Session = Depends(get_db)):
    # - `url: str`：用户传入的**目标爬取URL**（如豆瓣电影Top250的`https://movie.douban.com/top250`）
    # - `db: Session = Depends(get_db)`：通过**依赖注入**获取数据库会话（`get_db`负责创建/关闭数据库连接）

    """接口说明：触发爬虫，爬取数据并存储到数据库"""

    # 4. 调用核心爬虫函数，传入URL和数据库会话
    crawled_count = crawl_pet_medical_data(url, db)

    # 5. 返回响应（包含爬取数量和源URL）
    return {
        "message": f"成功爬取{crawled_count}条数据",  # 提示信息（文案可根据实际爬取对象调整）
        "source_url": url
    }