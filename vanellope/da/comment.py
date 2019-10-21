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

        params.append(data['email'])
        params.append(data['website'])

        assert data['content'] and len(data['content']) > 0
        params.append(data['content'])

        # state. possible values: checking, approved, banned
        params.append('approved' if data['is_admin'] else 'checking')

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
            created_at.strftime('%Y-%m-%d %H:%M:%S'))

        params.append(comment_id)
        params.append(created_at)

        cur.execute(sql, params)
        self.conn.commit()

        return comment_id

    def find(self, post_id_list=[], id_list=[], limit=None, skip=0, states=[]):
        sql = """
              SELECT
                  comments.uuid,
                  comments.post_id,
                  posts.title as post_title,
                  comments.name,
                  comments.email,
                  comments.content,
                  comments.state,
                  comments.created_at as "created_at [timestamp]"
              FROM comments
              LEFT JOIN posts ON posts.uuid = comments.post_id
              WHERE 1
              """

        id_list = list(filter(None, id_list))
        post_id_list = list(filter(None, post_id_list))
        states = list(filter(None, states))

        params = []

        if len(id_list) > 0:
            sql += " AND comments.uuid IN (?) "
            params.append(','.join(id_list))

        if len(post_id_list) > 0:
            sql += " AND posts.uuid IN (?) "
            params.append(','.join(post_id_list))

        # https://stackoverflow.com/a/1310001/2609042
        if len(states) > 0:
            sql += " AND comments.state IN (%s)" % ','.join('?' * len(states))
            params.extend(states)

        sql += 'ORDER BY comments.created_at ASC'

        if limit:
            sql += " LIMIT ?"
            params.append(limit)

        if skip:
            sql += " OFFSET ?"
            params.append(skip)

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [self.to_dict(cur, p) for p in cur.fetchall()]

    def count(self,
              tag_list=[],
              before_date=None,
              after_date=None,
              states=[],
              categories=[]):

        tag_list = list(filter(None, tag_list))
        states = list(filter(None, states))
        categories = list(filter(None, categories))

        sql = " SELECT count(*) as count FROM comments WHERE 1 "
        params = []

        if len(tag_list) > 0:
            sql += " AND tags LIKE "
            sql += ' OR '.join(['?'] * len(tag_list))
            params += ['%' + tag + '%' for tag in tag_list]

        if before_date:
            sql += " AND created_at <= ?"
            params.append(before_date)

        if after_date:
            sql += " AND created_at >= ?"
            params.append(after_date)

        # https://stackoverflow.com/a/1310001/2609042
        if len(states) > 0:
            sql += " AND state IN (%s)" % ','.join('?' * len(states))
            params.extend(states)

        if len(categories) > 0:
            sql += " AND category IN (?)"
            params.append(','.join(categories))

        sql += " ORDER BY created_at DESC"

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()[0]

    def update(self, uid, data):
        """Update comment by uuid
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []
        params.append(data['state'])

        cur = self.conn.cursor()

        sql = """
              UPDATE comments
              SET state = ?
              WHERE uuid = ?
              """
        params.append(uid)

        cur.execute(sql, params)
        self.conn.commit()


    def gen_uuid(self, post_id, email, content, timestamp):
        """Generate comment uuid based on conditions
        """

        m = hashlib.sha1()
        s = post_id + email + content + timestamp
        m.update(s.encode('utf-8'))
        uuid = m.hexdigest()[:8]
        return uuid
