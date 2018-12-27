# coding=utf-8

import hashlib
from vanellope.da import DataAccess, random_string
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
