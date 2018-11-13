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
from vanellope.da import DataAccess, session_connection
from tornado.util import ObjectDict


class Session(DataAccess):
    def __init__(self):
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_session (
                auth TEXT PRIMARY KEY,
                username TEXT
            )
        """)

        self.conn.commit()
        cur.close()

    @property
    def conn(self):
        return session_connection

    def set_user_session(self, auth, username):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO user_session
            (auth, username)
            VALUES (?, ?)
        """, (auth, username))
        self.conn.commit()
        cur.close()

    def get_user_session(self, auth):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM user_session
        """)
        username = cur.fetchall()
        try:
            return username[0]
        except:
            return None
