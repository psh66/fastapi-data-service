# app/api/v1/github_trending.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crawlers.spiders.github_trending_spider import crawl_github_trending
from app.data_cleaning.pipelines import clean_github_list
from app.data_cleaning.configs.github_clean_rules import GITHUB_CLEAN_RULES
from app.crawlers.utils.storage_utils import save_github_data

router = APIRouter()

@router.post("/crawl_github_trending")
def crawl_github(
    language: str = "",
    since: str = "daily",
    db: Session = Depends(get_db)
):
    """手动触发 GitHub Trending 爬取"""
    raw_data = crawl_github_trending(language=language, since=since)
    cleaned_data = clean_github_list(raw_data, GITHUB_CLEAN_RULES)
    save_github_data(cleaned_data, db)
    return {"message": "爬取成功", "count": len(cleaned_data)}