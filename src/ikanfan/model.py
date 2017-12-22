# coding: utf-8


import sqlite3


class PlayerEntry(object):
    def __init__(self):
        self.comic_id = None
        self.idx = None
        self.title = None
        self.player_config = None
        self.player_type = None


class ComicEntry(object):
    def __init__(self):
        self.comic_id = None
        self.player_list = {}
        self.title = None
        self.score = None
        self.introduce = None
        self.cover = None
        self.tag = None


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
            pass
        self._conn.close()
        return True
