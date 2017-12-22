# coding: utf-8

import logging
import traceback
import sqlite3

DB_ERR = object()


class PlayerEntry(object):
    __slots__ = ['idx', 'title', 'path', 'player_config', 'player_type']

    def __init__(self):
        self.idx = None
        self.title = None
        self.path = None
        self.player_config = None
        self.player_type = None

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
        self.score = None
        self.introduce = None
        self.cover = None
        self.tag = None
        self.category = None

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


class IKanFanDB(object):
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

    @staticmethod
    def parse(row, description):
        fields = [item[0] for item in description]
        ret = {}
        for i, val in enumerate(row):
            ret[fields[i]] = val
        return ret


if __name__ == '__main__':
    db = IKanFanDB('/tmp/data.db')
    print db.update('create table test(id integer primary key autoincrement, name char(3))')
    for i in range(10):
        print db.insert('insert into test (name) values(?)', str(i))
    print db.query('select * from test')
