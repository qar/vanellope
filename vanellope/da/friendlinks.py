# coding=utf-8

import os
import os.path
import uuid
from vanellope import config
from vanellope.da import DataAccess
from tornado.util import ObjectDict


class FriendLinkModel(DataAccess):
    """FriendLink Model
    """

    def create(self, data):
        """Create new friendlink
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []

        params.append(data['title'])
        params.append(data['address'])
        params.append(data['notes'])

        cur = self.conn.cursor()

        sql = """ INSERT INTO friendlinks
                  (title, address, notes, created_at, uuid)
                  VALUES (?, ?, ?, ?, ?)
              """

        params.append(datetime.datetime.now())
        link_id = uuid.uuid4()
        params.append(link_id)

        cur.execute(sql, params)
        self.conn.commit()

        return post_id

    def update(self, uid, data):
        """Update friendlink by it's id
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []

        params.append(data['title'])
        params.append(data['address'])
        params.append(data['notes'])

        cur = self.conn.cursor()

        sql = """
              UPDATE friendlinks
              SET title = ?,
                  address = ?,
                  notes = ?,
                  updated_at = ?
              WHERE uuid = ?
              """
        params.append(datetime.datetime.now())
        params.append(uid)

        cur.execute(sql, params)
        self.conn.commit()

    def find_all(self):

        sql = """
              SELECT title, address, notes,
                  posts.created_at as "created_at [timestamp]",
                  posts.updated_at
              FROM friendlinks
              """
        cur = self.conn.cursor()
        cur.execute(sql)
        return [self.__parse(self.to_dict(cur, p)) for p in cur.fetchall()]

    def remove(self, uid):
        """Delete from trash. can't be recovered
        """

        cur = self.conn.cursor()

        sql = """
              DELETE FROM friendlinks WHERE uuid = ?
              """
        cur.execute(sql, uid)
        self.conn.commit()
