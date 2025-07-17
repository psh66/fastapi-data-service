from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

# 创建简易演示路由
router = APIRouter()

# 模拟数据存储
items = []

# 数据模型
class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Optional[bool] = False

# 接口实现
@router.get("/items/", response_model=List[Item], tags=["演示接口"])
def read_items():
    return items

@router.get("/items/{item_id}", response_model=Item, tags=["演示接口"])
def read_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/", response_model=Item, status_code=201, tags=["演示接口"])
def create_item(item: Item):
    # 检查 ID 是否存在
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

@router.put("/items/{item_id}", response_model=Item, tags=["演示接口"])
def update_item(item_id: int, updated_item: Item):
    index = next((i for i, item in enumerate(items) if item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 更新数据（保持 ID 不变）
    items[index] = updated_item.copy(update={"id": item_id})
    return items[index]

@router.delete("/items/{item_id}", tags=["演示接口"])
def delete_item(item_id: int):
    global items
    initial_len = len(items)
    items = [item for item in items if item.id != item_id]
    
    if len(items) == initial_len:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item deleted successfully"}