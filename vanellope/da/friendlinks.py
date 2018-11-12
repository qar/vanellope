# coding=utf-8

import os
import os.path
import uuid
import datetime
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
                  (title, address, notes, created_at, updated_at, uuid)
                  VALUES (?, ?, ?, ?, ?, ?)
              """

        params.append(datetime.datetime.now())
        params.append(datetime.datetime.now())
        params.append(str(uuid.uuid4()))

        cur.execute(sql, params)
        self.conn.commit()
        return cur.lastrowid

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
        return self.conn.commit()

    def find_all(self):

        sql = """
              SELECT uuid, title, address, notes,
                  friendlinks.created_at as "created_at [timestamp]",
                  friendlinks.updated_at as "updated_at [timestamp]"
              FROM friendlinks
              """
        cur = self.conn.cursor()
        cur.execute(sql)
        return [self.to_dict(cur, p) for p in cur.fetchall()]

    def remove(self, uid):
        """Delete from trash. can't be recovered
        """

        cur = self.conn.cursor()

        sql = """
              DELETE FROM friendlinks WHERE uuid = ?
              """
        cur.execute(sql, [uid])
        self.conn.commit()
