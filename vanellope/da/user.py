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


class UserModel(DataAccess):
    def __init__(self):
        pass

    def create(self, data):
        cur = self.conn.cursor()
        sql = """
            INSERT INTO users
            (username, passwd, salt, role)
            VALUES (?, ?, ?, ?)
        """

        salt = random_string(8)
        passwd_hash = hashlib.sha256(data['password'] + salt).hexdigest()

        cur.execute(sql, (data['username'], passwd_hash, salt, data['role']))
        self.conn.commit()
        return passwd_hash

    def create_user(self, data):
        cur = self.conn.cursor()
        sql = """
            INSERT INTO users
            (username, email, passwd, salt, role)
            VALUES (?, ?, ?, ?, ?)
        """

        salt = random_string(8)
        passwd_hash = hashlib.sha256(data['password'] + salt).hexdigest()

        cur.execute(sql, (
            data['username'],
            data['email'],
            passwd_hash,
            salt,
            data['role']
        ))
        self.conn.commit()
        return passwd_hash

    def get_admin_user(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM users WHERE role="admin" AND username="Admin"
        """)

        admin_user = self.to_dict(cur, cur.fetchone())
        if admin_user is not None:
            admin_user = ObjectDict(admin_user)

        return admin_user
