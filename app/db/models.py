from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # login_name = Column(String(50), unique=True, nullable=False, index=True)  # 长度50、唯一、必填、加索引
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")

class PetDisease(Base):
    __tablename__ = "pet_diseases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)  # 疾病名称
    symptoms = Column(Text, nullable=False)  # 清洗后的症状描述
    source_url = Column(String(255))  # 爬取数据的来源URL