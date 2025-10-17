from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from jose import JWTError  # 从jose导入JWTError，与security.py保持一致
from app.db.session import get_db 
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import User, UserCreate
from app.api.deps import  get_current_user,UserRequest  # 如需权限控制，与 item 保持一致
from app.core.security import (
    verify_password, 
    create_access_token, 
    decode_token  # 使用security.py中已实现的decode_token
)
from app.core.config import settings  # 从配置文件获取密钥等信息
from app.schemas.auth import LoginRequest
router = APIRouter()

# 1. 定义用户信息模型（建议使用Pydantic模型更规范）
class UserRequest:
    def __init__(self, user_id: str, email: str, role: str = "user"):
        self.user_id = user_id
        self.email = email
        # self.role = role

# 2. 优化认证依赖函数（使用security.py中的decode_token）
# def get_current_user(
#     Authorization: str = Header(None),
#     db: Session = Depends(get_db)
# ) -> UserRequest:
    # """解析Bearer令牌，验证并返回当前用户"""
    # if not Authorization:
    #     raise HTTPException(
    #         status_code=401,
    #         detail="未提供Authorization头",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    # try:
    #     # 提取Bearer令牌（格式：Bearer <token>）
    #     token = Authorization.split(" ")[1]
    #     # 使用security.py中已实现的decode_token解析
    #     payload = decode_token(token)
    #     if not payload:  # decode_token返回空字典表示解析失败
    #         raise HTTPException(status_code=401, detail="令牌无效")
        
    #     email: str = payload.get("sub")
    #     if not email:
    #         raise HTTPException(status_code=401, detail="令牌中未包含用户信息")
        
    #     # 查询用户是否存在
    #     user = get_user_by_email(db, email=email)
    #     if not user:
    #         raise HTTPException(status_code=401, detail="用户不存在")
        
    #     return UserRequest(user_id=str(user.id), email=user.email)
    
    # except (JWTError, IndexError):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="无效的令牌或令牌格式错误（正确格式：Bearer <token>）",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

# 3. 登录接口（保持不变，已适配create_access_token）
@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 4. 注册接口（保持不变）
@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已注册")
    return create_user(db=db, user=user)

# 5. 示例：需要认证的接口（添加依赖后Swagger会显示Authorization）
@router.get("/profile")
def get_profile(current_user: UserRequest = Depends(get_current_user)):
    """获取当前登录用户的个人信息（需要认证）"""
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "message": "这是需要认证才能访问的接口"
    }
