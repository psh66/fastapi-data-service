from fastapi import Depends, HTTPException, status, Header
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional  # 新增：用于处理可选参数

from app.db.session import get_db
from app.db.models import User  # 数据库用户模型
from app.core.security import decode_token
from app.crud.user import get_user_by_email


# 1. 规范用户信息模型
class UserRequest(BaseModel):
    user_id: str
    email: str
    # role: str = "user"

    class Config:
        orm_mode = True  # 支持从ORM模型转换


# 2. 定义Bearer认证方案
bearer_scheme = HTTPBearer()


# 3. 认证依赖（同时支持全局认证和单个接口参数）
def get_current_user(
    # 新增：显式声明Authorization头依赖，使单个接口显示该参数
    Authorization: Optional[str] = Header(None),
    # 保留：通过安全方案获取令牌，用于全局Authorize按钮
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> UserRequest:
    """解析Bearer令牌，验证并返回当前用户"""
    try:
        # 兼容两种认证方式：优先使用Header中的令牌，否则使用安全方案的令牌
        if Authorization:
            # 处理格式：Bearer <token>
            token = Authorization.split(" ")[1]
        else:
            # 从安全方案获取令牌（全局认证按钮填入的令牌）
            token = credentials.credentials
        
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="令牌无效")
        
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="令牌中未包含用户信息")
        
        user = get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        
        # 验证用户状态
        if not user.is_active:
            raise HTTPException(status_code=403, detail="用户已被禁用")
        
        return UserRequest(user_id=str(user.id), email=user.email)
    
    except (JWTError, IndexError):
        raise HTTPException(
            status_code=401,
            detail="无效的令牌或格式错误（正确格式：Bearer <token>）",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 4. 活跃用户依赖（类型匹配）
def get_current_active_user(
    current_user: UserRequest = Depends(get_current_user)
) -> UserRequest:
    """获取当前活跃用户"""
    return current_user
