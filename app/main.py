from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router
print("API Router:", api_v1_router)  # 调试打印
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI CRUD Base!"}