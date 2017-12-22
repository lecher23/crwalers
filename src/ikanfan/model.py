# coding: utf-8

import logging
import traceback
import sqlite3


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
