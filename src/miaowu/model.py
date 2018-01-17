# coding: utf-8

from __future__ import unicode_literals
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Base.__table_args__ = {'mysql_character_set': 'utf8mb4'}


class Comic(Base):
    __tablename__ = 'comic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    outer_id = Column(Integer, unique=True, nullable=False, comment='动漫外部ID, 指在被爬的网站的ID')
    name = Column(String(32), nullable=False, comment='动漫标题')
    info = Column(String(128), default='', comment='动漫简介')
    detail = Column(String(1024), default='', comment='动漫详情')
    score = Column(Integer, default=0, comment='动漫评分, 百分制')
    cover = Column(String(256), default='')
    weight = Column(Integer, default=0, comment='动漫权重, 用来进行推荐排序')
    year = Column(Integer, default=0, comment='出版年份')


class CategoryDefine(Base):
    __tablename__ = 'category_define'
    cate_id = Column(Integer, primary_key=True, autoincrement=True, comment='分类ID')
    cate_name = Column(String(16), unique=True, nullable=False, comment='分类名称')


class Rank(Base):
    __tablename__ = 'rank'
    id = Column(Integer, primary_key=True, comment='排名的名次')
    comic_id = Column(Integer, comment='动漫ID')


class ComicTag(Base):
    __tablename__ = 'comic_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, nullable=False)
    tag_name = Column(String(16), nullable=False, comment='动漫标签')


class ComicCategory(Base):
    __tablename__ = 'comic_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, nullable=False)
    cate_id = Column(Integer, nullable=False, comment='动漫分类')


class ComicVideo(Base):
    __tablename__ = 'comic_video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, nullable=False)
    source = Column(String(8), nullable=False, comment='视频来源(爱奇艺、优酷等)')
    idx = Column(Integer, nullable=False, comment='哪一集')
    url = Column(String(128), nullable=False, comment='跳转链接')
    title = Column(String(128), default='', comment='本集标题')


if __name__ == '__main__':
    engine = create_engine('mysql+mysqldb://licheng:Cg123456@192.168.0.253:3306/dongman?charset=utf8')
    SessionCls = sessionmaker(bind=engine)
    session = SessionCls()
    Base.metadata.create_all(engine)
