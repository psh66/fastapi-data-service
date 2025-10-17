from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import get_users, create_user, get_user  # 新增用户相关的 CRUD 函数
from app.schemas.user import User, UserCreate
from app.api.deps import  get_current_user  # 如需权限控制，与 item 保持一致
from app.db.models import User as DBUser

router = APIRouter()

# 查询用户列表（参考 item 的 read_items）
@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: DBUser = Depends(get_current_user)):  # 添加登录依赖
    users = get_users(db, skip=skip, limit=limit)
    return users

# 创建用户（如需权限控制，参考 item 的 create_item）
@router.post("/", response_model=User)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    # 可选：如果创建用户需要权限（如管理员），添加如下依赖
    # current_user: DBUser = Depends(get_current_active_user)
):
    return create_user(db=db, user=user)  # 无需 user_id，用户是独立资源

# 查询单个用户（参考 item 的 read_item）
@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db),current_user: DBUser = Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user