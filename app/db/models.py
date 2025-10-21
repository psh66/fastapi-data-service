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


class ZhihuHot(Base):  # 继承Base基类（SQLAlchemy要求，用于注册模型元数据）
    __tablename__ = "zhihu_hot"  # 数据库表名（必须小写，下划线分隔，与模型名对应）
    # 主键id（自增，唯一标识每条数据，数据库自动维护）
    id = Column(Integer, primary_key=True, index=True)
    # 热榜排名（整数类型，对应清洗后的rank字段，必须是int）
    rank = Column(Integer, comment="热榜排名")
    # 热榜标题（字符串，最长500字符，对应清洗后title字段）
    title = Column(String(500), comment="热榜标题")
    # 热度值（字符串，如"100.5万"，对应清洗后hot_value字段）
    hot_value = Column(String(50), comment="热度值")
    # 热榜链接（完整URL，字符串，对应清洗后url字段）
    url = Column(String(500), comment="热榜链接")
    # 爬取时间（自动填充当前时间，无需清洗后数据提供，方便追溯）
    crawl_time = Column(DateTime, default=datetime.now, comment="爬取时间")

class GitHubTrending(Base):
    __tablename__ = "github_trending"
    id = Column(Integer, primary_key=True, index=True)
    # repo_name = Column(String(255), unique=True, index=True, comment="项目名称（owner/repo）")
    repo_name = Column(String(255), index=True, comment="项目名称（owner/repo）")
    repo_url = Column(String(255), comment="项目链接")
    description = Column(String(500), comment="项目描述")
    language = Column(String(50), comment="主编程语言")
    stars = Column(Integer, comment="星标数")
    forks = Column(Integer, comment="Fork 数")
    today_stars = Column(Integer, comment="今日新增星标数")
    crawl_time = Column(DateTime, default=datetime.now, comment="爬取时间")