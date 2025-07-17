from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.item import get_items, create_user_item, get_item
from app.crud.user import get_user
from app.schemas.item import Item, ItemCreate
from app.api.deps import get_current_active_user
from app.db.models import User

router = APIRouter()

@router.get("/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=Item)
def create_item(
    item: ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    return create_user_item(db=db, item=item, user_id=current_user.id)

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_item