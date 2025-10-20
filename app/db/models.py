from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Text,Float, Integer ,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
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
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    intro = Column(String(500))
    rating = Column(Float)
    source_url = Column(String(255))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    price = Column(Float)
    comment_count = Column(Integer)
    source_url = Column(String(255))


class ZhihuHot(Base):
    __tablename__ = "zhihu_hot"  # 表名
    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, comment="热榜排名")  # 排名（整数）
    title = Column(String(500), comment="热榜标题")  # 标题（长文本）
    hot_value = Column(String(50), comment="热度值")  # 热度（如“100.5万”）
    url = Column(String(500), comment="热榜链接")  # 完整URL
    crawl_time = Column(DateTime, default=datetime.now, comment="爬取时间")  # 记录爬取时间
