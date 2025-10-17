from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. 导入跨域中间件
from app.api.v1.router import router as api_v1_router
print("API Router:", api_v1_router)
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base
from app.core.security import oauth2_scheme
from app.api.deps import bearer_scheme

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    security=[{"HTTPBearer": []}]
)

# 2. 新增：直接添加跨域中间件（全局生效）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境用通配符，生产环境替换为前端域名（如 ["http://localhost:8080"]）
    allow_credentials=True,  # 允许携带 Token/Cookie，适配你的 JWT 认证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头（含 Authorization）
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI CRUD Base!"}