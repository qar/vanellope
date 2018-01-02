# coding=utf-8

import os
import os.path
import calendar
import zipfile
import datetime
import random
import sqlite3
import string
import hashlib
import time
from vanellope import config
from vanellope.da import DataAccess
from tornado.util import ObjectDict


class ConfigModel(DataAccess):
    """ Site configuration
    """

    # 网站的全部配置
    # 使用 Tornado 提供的 ObjectDict，
    # 可以使用 . 运算符读取属性
    config = ObjectDict()

    def __init__(self):
        super(DataAccess, self).__init__()

    def read_config(self):
        cur = self.conn.cursor()
        results = cur.execute("SELECT * FROM configuration").fetchall()

        configs = {}
        if results:
            results = [self.to_dict(cur, item) for item in results]

        for r in results:
            configs[r['key']] = r['value']

        return configs

    def set_value(self, k, v):
        sql = """
            UPDATE config SET value = ? WHERE key = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (v, k))
        self.conn.commit()
        return

    def get_value(self, k):
        sql = """
            SELECT value FROM config WHERE key = ?
        """

        cur = self.conn.cursor()
        cur.execute(sql, (k,))
        return cur.fetchone()

    @property
    def site_name(self):
        site_name = self.get_value('site_name')
        return site_name[0]

    def update(self, data):
        cur = self.conn.cursor()
        t = tuple((v, k) for k, v in data.items())
        cur.executemany("UPDATE configuration SET value = ? WHERE key = ?", t)
