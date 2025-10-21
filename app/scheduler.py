from apscheduler.schedulers.blocking import BlockingScheduler
from app.db.session import engine, Base  # 从 session.py 导入 Base（关键修改）
from app.db.models import GitHubTrending
from app.crawlers.spiders.github_trending_spider import crawl_github_trending
from app.data_cleaning.pipelines import clean_github_list
from app.data_cleaning.configs.github_clean_rules import GITHUB_CLEAN_RULES
from app.crawlers.utils.storage_utils import save_github_data
from app.db.session import get_db

def init_db():
    """初始化数据库表（首次运行时创建）"""
    Base.metadata.create_all(bind=engine)  # 这里的 Base 已从 session.py 导入

def daily_github_crawl():
    """每日爬取任务：爬取今日热门项目"""
    init_db()
    db = next(get_db())
    raw_data = crawl_github_trending(since="daily")
    cleaned_data = clean_github_list(raw_data, GITHUB_CLEAN_RULES)
    save_github_data(cleaned_data, db)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 每天凌晨 3 点执行爬取
    scheduler.add_job(daily_github_crawl, "cron", hour=3, minute=0)
    print("GitHub Trending 定时爬虫启动，每天凌晨 3 点自动爬取")
    scheduler.start()