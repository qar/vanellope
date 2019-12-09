# coding=utf-8

import hashlib
import datetime
from vanellope.da import DataAccess, random_string
from tornado.util import ObjectDict
from utils import randomwords


class UserModel(DataAccess):
    def __init__(self):
        pass

    def set_secret_key(self, username):
        cur = self.conn.cursor()
        secret_key = randomwords(20)

        sql = """
              UPDATE users
              SET secret_key = ?,
                  updated_at = ?
              WHERE username = ?
              """
        params = [
            secret_key,
            datetime.datetime.now(),
            username
        ]

        cur.execute(sql, params)
        self.conn.commit()
        return secret_key

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
        passwd_hash = hashlib.sha256((data['password'] + salt).encode('utf-8')).hexdigest()

        cur.execute(sql, (
            data['username'],
            data['email'],
            passwd_hash,
            salt,
            data['role']
        ))
        self.conn.commit()
        return passwd_hash

    def get_user_by_name(self, username):
        """Get user by username
        """
        cur = self.conn.cursor()
        sql = """
            SELECT * FROM users WHERE username = ?
        """
        cur.execute(sql, [username])
        user = self.to_dict(cur, cur.fetchone())
        return user

    def get_admin_user(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM users WHERE role="admin" AND username="Admin"
        """)

        admin_user = self.to_dict(cur, cur.fetchone())
        if admin_user is not None:
            admin_user = ObjectDict(admin_user)

        return admin_user

    def update_user_by_username(self, username, profile):
        """Update user profile by username
        """

        # cur = self.conn.cursor()
        # t = tuple((v, k) for k, v in profile.items())
        # cur.executemany("UPDATE users SET value = ? WHERE key = ?", t)

        if type(profile) is not dict:
            raise TypeError('parameter `profile` must be a dict object')

        params = []

        params.append(profile['email'])

        cur = self.conn.cursor()

        sql = """
              UPDATE users
              SET email = ?,
                  updated_at = ?
              WHERE username = ?
              """
        params.append(datetime.datetime.now())
        params.append(username)

        cur.execute(sql, params)
        self.conn.commit()

    def verify_email(self, token):
        cur = self.conn.cursor()
        sql = """
              UPDATE users
              SET email_verified = 'yes',
                  updated_at = ?
              WHERE secret_key = ?
              """
        params = [
            datetime.datetime.now(),
            token
        ]
        cur.execute(sql, params)
        self.conn.commit()
