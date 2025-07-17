from pydantic_settings import BaseSettings  # 修改导入位置

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI CRUD Base"
    API_V1_STR: str = "/api/v1"
    
    # JWT 认证配置
    SECRET_KEY: str = "your-secret-key"  # 生产环境需替换为安全随机字符串
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"
    
    class Config:
        case_sensitive = True

settings = Settings()