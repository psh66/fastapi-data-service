from fastapi import APIRouter
from app.api.v1.endpoints import auth, items ,demo,users


router = APIRouter()
router.include_router(auth.router, prefix="", tags=["auth"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(users.router,prefix='/users',tags=['users'])
router.include_router(demo.router, prefix="/demo", tags=["测试接口"])  # 新增演示路由
