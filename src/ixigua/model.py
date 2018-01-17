# coding: utf-8

from __future__ import unicode_literals
import logging
import json

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_ERR = type(str('DBErrCls'), (object,), {'__nonzero__': lambda self: False})()

Base = declarative_base()
Base.__table_args__ = {'mysql_character_set': 'utf8mb4'}


class XiguaVideo(Base):
    __tablename__ = 'xigua_video'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False, comment='视频标题')
    description = Column(String(128), default='', comment='视频简介')
    tag = Column(String(32), default='', comment='视频标签')
    author = Column(String(32), default='', comment='视频发布者')
    video_id = Column(String(32), default='', comment='视频ID')
    comment_num = Column(Integer, default=0, comment='视频评论数')
    access_url = Column(String(256), default='', comment='访问页面')
    duration = Column(Integer, default=0, comment='视频时长')
    cover = Column(String(256), default='', comment='视频封面')
    video_url = Column(String(256), default='', comment='视频地址')

    def __repr__(self):
        raw = {
            'title': self.title,
            'desc': self.description,
            'author': self.author,
            'tag': self.tag,
            'id': self.video_id,
            'count': self.comment_num,
            'page': self.access_url,
            'time': self.duration,
            'cover': self.cover,
            'video': self.video_url
        }
        s = ''
        try:
            s = json.dumps(raw, ensure_ascii=False, indent=2).encode('utf-8')
        except:
            logging.exception('repr VideoInf failed.')
        return s


class VideoInf(object):
    def __init__(self):
        self.title = None
        self.description = None
        self.tag = None
        self.author = None
        self.video_id = None
        self.watched_num = None
        self.access_url = None
        self.duration = None
        self.cover = None
        self.video_url = None

    def __repr__(self):
        raw = {
            'title': self.title,
            'desc': self.description,
            'author': self.author,
            'tag': self.tag,
            'id': self.video_id,
            'count': self.watched_num,
            'page': self.access_url,
            'time': self.duration,
            'cover': self.cover,
            'video': self.video_url
        }
        s = 'error'
        try:
            s = json.dumps(raw, ensure_ascii=False, indent=2).encode('utf-8')
        except:
            logging.exception('repr VideoInf failed.')
        return s


if __name__ == '__main__':
    engine = create_engine('mysql+mysqldb://licheng:Cg123456@192.168.0.253:3306/downline?charset=utf8')
    SessionCls = sessionmaker(bind=engine)
    session = SessionCls()
    Base.metadata.create_all(engine)
