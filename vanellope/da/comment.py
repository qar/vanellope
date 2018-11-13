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


class CommentModel(DataAccess):
    """
    """

    __comment = None

    def create(self, data):
        """Create new comment
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []

        assert data['post_id'] and len(data['post_id']) > 0
        params.append(data['post_id'])

        assert data['name'] and len(data['name']) > 0
        params.append(data['name'])

        assert data['email'] and len(data['email']) > 0
        params.append(data['email'])

        params.append(data['website'])

        assert data['content'] and len(data['content']) > 0
        params.append(data['content'])

        # state. possible values: checking, pass, denied
        params.append('pass')

        cur = self.conn.cursor()

        sql = """ INSERT INTO comments
                  (post_id, name, email, website, content,
                   state, uuid, created_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
              """

        created_at = datetime.datetime.now()

        # One person posting the same comment under the same article
        # in one hour is forbidden
        comment_id = self.gen_uuid(
            data['post_id'],
            data['email'],
            data['content'],
            created_at.strftime('%Y-%m-%d %H'))

        params.append(comment_id)
        params.append(created_at)

        cur.execute(sql, params)
        self.conn.commit()

        return comment_id

    def find(self, post_id, state):
        sql = """
              SELECT
                  uuid,
                  post_id,
                  name,
                  email,
                  content,
                  state,
                  created_at as "created_at [timestamp]"
              FROM comments WHERE post_id = ? AND state = ?
              ORDER BY created_at ASC
              """
        params = [post_id, state]

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [self.to_dict(cur, p) for p in cur.fetchall()]

    def gen_uuid(self, post_id, email, content, timestamp):
        """Generate comment uuid based on conditions
        """

        m = hashlib.sha1()
        s = post_id + email + content + timestamp
        m.update(s.encode('utf-8'))
        uuid = m.hexdigest()[:8]
        return uuid
