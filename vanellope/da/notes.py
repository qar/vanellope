# coding=utf-8

import datetime
import hashlib
import time
from vanellope.da import DataAccess


class NoteModel(DataAccess):
    """
    """

    def __parse(self, item):
        return item

    def create(self, data):
        """Create new note
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []
        params.append(data['content'])
        cur = self.conn.cursor()

        sql = """ INSERT INTO notes
                  (content, uuid, created_at, updated_at)
                  VALUES (?, ?, ?, ?)
              """

        uid = self.gen_uuid(data['content'])
        params.append(uid)
        params.append(datetime.datetime.now())
        params.append(datetime.datetime.now())

        cur.execute(sql, params)
        self.conn.commit()

        return uid

    def gen_uuid(self, content):
        """Generate uuid based content and timestamp
        """

        m = hashlib.sha1()
        s = content + str(time.time())
        m.update(s.encode('utf-8'))
        uuid = m.hexdigest()[:8]
        return uuid

    def find(self, limit=None, skip=0, before_date=None, after_date=None):
        sql = """
              SELECT
                  uuid,
                  content,
                  notes.created_at as "created_at [timestamp]",
                  notes.updated_at

              FROM notes

              WHERE 1
              """
        params = []

        if before_date:
            sql += " AND notes.created_at <= ?"
            params.append(before_date)

        if after_date:
            sql += " AND notes.created_at >= ?"
            params.append(after_date)

        sql += " ORDER BY notes.created_at DESC"

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
        sql = " SELECT count(*) as count FROM notes WHERE 1 "
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
