from fastapi import APIRouter
from app.api.v1.endpoints import auth, items ,demo,users
from app.crawlers.api import router as crawlers_router
from app.api.v1 import github_trending  # 导入新增的 GitHub 路由
router = APIRouter()
# 注册爬虫路由
router.include_router(crawlers_router, tags=["pach"])

router.include_router(github_trending.router, prefix="/v1", tags=["gib"])  # 注册 GitHub 路由
router.include_router(auth.router, prefix="", tags=["auth"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(users.router,prefix='/users',tags=['users'])
router.include_router(demo.router, prefix="/demo", tags=["测试接口"])  # 新增演示路由


