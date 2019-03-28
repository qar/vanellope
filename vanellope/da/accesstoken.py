# coding=utf-8

import calendar
import datetime
import hashlib
import time
import uuid
from vanellope import config
from vanellope.da import DataAccess


class AccessTokenModel(DataAccess):
    """
    """

    def __parse(self, item):
        return item

    def create(self):
        """Create new access token
        """

        params = [
            str(uuid.uuid4()),
            datetime.datetime.now()
        ]

        cur = self.conn.cursor()

        sql = """ INSERT INTO tokens
                  (token, created_at)
                  VALUES (?, ?)
              """

        cur.execute(sql, params)
        self.conn.commit()
        return params[0]

    def find(self, limit=None, skip=0, before_date=None, after_date=None):

        sql = """
              SELECT
                  token,
                  tokens.created_at as "created_at [timestamp]"

              FROM tokens

              WHERE 1
              """
        params = []

        if before_date:
            sql += " AND tokens.created_at <= ?"
            params.append(before_date)

        if after_date:
            sql += " AND tokens.created_at >= ?"
            params.append(after_date)

        sql += " ORDER BY tokens.created_at DESC"

        if limit:
            sql += " LIMIT ?"
            params.append(limit)

        if skip:
            sql += " OFFSET ?"
            params.append(skip)

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [self.__parse(self.to_dict(cur, p)) for p in cur.fetchall()]

    def count(self, before_date=None, after_date=None):
        sql = " SELECT count(*) as count FROM tokens WHERE 1 "
        params = []

        if before_date:
            sql += " AND created_at <= ?"
            params.append(before_date)

        if after_date:
            sql += " AND created_at >= ?"
            params.append(after_date)

        sql += " ORDER BY created_at DESC"

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()[0]

    def validate(self, token):
        sql = "SELECT * FROM tokens WHERE token = ?"
        cur = self.conn.cursor()
        cur.execute(sql, [token])
        if not cur.fetchone():
            raise Exception('token is not valid');

    def remove(self, token):
        cur = self.conn.cursor()

        sql = """
              DELETE FROM tokens
              WHERE token = ?
              """
        params = [token]

        cur.execute(sql, params)
        self.conn.commit()

