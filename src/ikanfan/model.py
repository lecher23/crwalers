# coding: utf-8

import logging
import traceback
import sqlite3

DB_ERR = type('DBErrCls', (object,), {'__bool__': lambda self: False})()


class PlayerEntry(object):
    __slots__ = ['comic_id', 'idx', 'title', 'path', 'config_str', 'player_type']

    def __init__(self):
        self.comic_id = None
        self.idx = None
        self.title = None
        self.path = None
        self.config_str = None
        self.player_type = None

    @staticmethod
    def table_sql():
        return '''create table video(
        video_id integer primary key autoincrement,
        comic_id int not null,
        idx varchar(15) not null,
        title varchar(63) not null,
        path varchar(63) not null,
        config_str varchar(1023) not null,
        player_type varchar(31) not null
        )'''

    @staticmethod
    def save_sql():
        return '''insert into video(comic_id, idx, title, path, config_str, player_type) values (?,?,?,?,?,?)'''

    @staticmethod
    def query_sql():
        return '''select title from video where path=?'''

    @staticmethod
    def update_sql():
        return '''update video set config_str=? where path=?'''

    @staticmethod
    def table_name():
        return 'video'

    def __repr__(self):
        return "PlayerEntry({})".format(
            ','.join(['%r=%r' % (item, getattr(self, item, '')) for item in self.__slots__]))


class ComicEntry(object):
    __slots__ = ['comic_id', 'page_path', 'players', 'name', 'score', 'introduce', 'cover', 'tag', 'category']

    def __init__(self):
        self.comic_id = None
        self.page_path = None
        self.players = {}
        self.name = None
        self.score = 0
        self.introduce = ''
        self.cover = None
        self.tag = None
        self.category = None

    @staticmethod
    def table_sql():
        return '''create table comic(
        comic_id int primary key,
        page_path varchar(63) not null,
        name varchar(63) not null,
        score int default 0,
        introduce varchar(255) not null,
        cover varchar(255) not null,
        tag varchar(31) not null,
        category char(8) not null
        )'''

    @staticmethod
    def save_sql():
        return '''insert into comic values (?,?,?,?,?,?,?,?)'''

    @staticmethod
    def query_sql():
        return '''select name from comic where comic_id=?'''

    @staticmethod
    def update_sql():
        return '''update comic set page_path=?, name=?, score=?,introduce=?, cover=? where comic_id=?'''

    @staticmethod
    def table_name():
        return 'comic'

    def __repr__(self):
        return "ComicEntry({})".format(
            ','.join(['%r=%r' % (item, getattr(self, item)) for item in self.__slots__]))


class ConnWrapper(object):
    def __init__(self, db):
        self._db_file = db
        self._conn = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._db_file)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            logging.warning('run sql failed. %s -> %s', exc_val, traceback.extract_tb(exc_tb))
        self._conn.close()
        return True


class SqliteWrapper(object):
    def __init__(self, db_file):
        self._db_file = db_file

    @property
    def connection(self):
        return ConnWrapper(self._db_file)

    def insert(self, sql, *args):
        ret = DB_ERR
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(sql, args)
            ret = cursor.lastrowid
        return ret

    def update(self, sql, *args):
        ret = DB_ERR
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(sql, args)
            ret = cursor.rowcount
        return ret

    def get(self, q, *args):
        ret = DB_ERR
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(q, args)
            db_ret = cursor.fetchall()
            if not db_ret:
                ret = None
            elif len(db_ret) > 1:
                raise RuntimeError('too many result.')
            else:
                ret = self.parse(db_ret[0], cursor.description)
        return ret

    def query(self, q, *args):
        ret = DB_ERR
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(q, args)
            db_ret = cursor.fetchall()
            ret = []
            for row in db_ret:
                ret.append(self.parse(row, cursor.description))
        return ret

    def get_tables(self):
        ret = self.query('select name from sqlite_master where type=\'table\' order by name')
        if ret != DB_ERR:
            return [item['name'] for item in ret]
        raise RuntimeError('获取数据库表失败')

    @staticmethod
    def parse(row, description):
        fields = [item[0] for item in description]
        ret = {}
        for i, val in enumerate(row):
            ret[fields[i]] = val
        return ret


class IKanFanDB(SqliteWrapper):
    def __init__(self, db_file):
        super(IKanFanDB, self).__init__(db_file)
        self.init_database()

    def save_comic(self, entry):
        ret = self.get(ComicEntry.query_sql(), entry.comic_id)
        if ret is not DB_ERR and ret:
            print self.update(ComicEntry.update_sql(), entry.page_path, entry.name, entry.score,
                              entry.introduce, entry.cover, entry.comic_id)
        else:
            print self.insert(
                ComicEntry.save_sql(), entry.comic_id, entry.page_path, entry.name,
                entry.score, entry.introduce, entry.cover, entry.tag, entry.category)
        for player_name, video_list in entry.players.items():
            logging.warning('save video for %s', player_name)
            for video in video_list:
                self.save_video(video)

    def save_video(self, entry):
        ret = self.get(PlayerEntry.query_sql(), entry.path)
        if ret is not DB_ERR and ret:
            print self.update(PlayerEntry.update_sql(), entry.config_str, entry.path)
        else:
            print self.insert(
                PlayerEntry.save_sql(), entry.comic_id, entry.idx, entry.title,
                entry.path, entry.config_str, entry.player_type)

    def init_database(self):
        tbs = self.get_tables()
        self._create_table(PlayerEntry, tbs)
        self._create_table(ComicEntry, tbs)

    def _create_table(self, cls, existed_tables):
        if cls.table_name() not in existed_tables:
            ret = self.update(cls.table_sql())
            if ret == DB_ERR:
                raise RuntimeError('创建表 %s 失败' % cls.table_name())


if __name__ == '__main__':
    # db = SqliteWrapper('/tmp/data.db')
    # print db.get_tables()
    # print db.query('select name from sqlitemaster where ')
    # print db.update('create table test(id integer primary key autoincrement, name char(3))')
    # for i in range(10):
    #     print db.insert('insert into test (name) values(?)', str(i))
    # print db.query('select * from test')
    db = IKanFanDB('/tmp/data.db')
    en = ComicEntry()
    en.comic_id = 99
    en.cover = 'cover'
    en.score = 10
    en.page_path = '/move/99.html'
    en.category = 'hot blood'
    en.name = 'seven dragon ball'
    en.tag = '200'
    db.save_comic(en)
    en2 = PlayerEntry()
    en2.comic_id = en.comic_id
    en2.config_str = 'lalalal'
    en2.player_type = '233'
    en2.idx = '10'
    en2.path = '666'
    en2.title = u'快来看呀'
    db.save_video(en2)
