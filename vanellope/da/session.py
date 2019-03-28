# coding=utf-8

import os
import os.path
import calendar
import zipfile
import datetime
import uuid
import random
import sqlite3
import string
import hashlib
import time
from datetime import timedelta
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                sid TEXT PRIMARY KEY,
                name TEXT NOT NULL DEFAULT '_anonymous_',
                ip TEXT,
                useragent TEXT,
                requests INTEGER NOT NULL DEFAULT 1,
                expire TIMESTAMP NOT NULL
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

    def check_visitor(self, session_id):
        cur = self.conn.cursor()
        sql = """
            SELECT * FROM visitors WHERE sid = ?
        """
        cur.execute(sql, [session_id])
        return self.to_dict(cur, cur.fetchone())

    def record_visitor(self, session_id, username, ip, useragent):
        cur = self.conn.cursor()
        sql = """
            INSERT INTO visitors
            (sid, name, ip, useragent, expire)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (sid) DO UPDATE
            SET requests=requests+1
        """

        params = []
        params.append(session_id)
        params.append(username)
        params.append(ip)
        params.append(useragent)
        params.append(datetime.datetime.now() + timedelta(seconds=5))

        cur.execute(sql, params)
        self.conn.commit()

    def scan(self):
        """Delete all expired rows from visitors
        """
        cur = self.conn.cursor()
        sql = """
            DELETE FROM visitors WHERE expire <= ?
        """
        cur.execute(sql, [datetime.datetime.now()])
        self.conn.commit()

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
