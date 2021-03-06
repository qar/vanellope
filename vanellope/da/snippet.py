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


class SnippetModel(DataAccess):
    """
    """

    __post = None

    def __parse(self, item):
        if 'tags' in item:
            tags = item['tags'].split(',')
            item['tags'] = filter(None, [t.strip() for t in tags])

        if item['state'] == 'draft':
            item['path'] = ''.join([
                config.app_settings['draft_base_path'],
                item['uuid'],
                '+',
                u'_'.join(item['title'].split())
            ])

        elif item['state'] == 'published':
            item['path'] = ''.join([
                '/article/',
                item['uuid'],
                '+',
                u'_'.join(item['title'].split())
            ])

        elif item['state'] == 'deleted':
            item['path'] = ''.join([
                '/trash/',
                item['uuid'],
                '+',
                u'_'.join(item['title'].split())
            ])

        item['editor-path'] = ''.join([
            '/admin/edit/',
            item['uuid'],
            '+',
            u'_'.join(item['title'].split())
        ])

        return item

    def create(self, data):
        """Create new post
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []

        assert data['ext']
        assert data['ext'] == 'html'
        params.append(data['ext'])

        assert data['title'] and len(data['title']) > 0
        params.append(data['title'])

        assert data['source'] and len(data['source']) > 0
        params.append(data['source'])

        assert data['content'] and len(data['content']) > 0
        params.append(data['content'])

        if 'category' in data:
            category = data['category']
        else:
            category = config.app_settings['default_category']

        params.append(category)

        tags_str = ','.join(data['tags']) if 'tags' in data else ''
        params.append(','.join(['', tags_str, '']))
        params.append(data['state'])

        cur = self.conn.cursor()

        sql = """ INSERT INTO posts
                  (ext, title, source, content, category, tags,
                   state, uuid, created_at, updated_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """

        post_id = self.gen_uuid(data['title'], data['content'])
        params.append(post_id)
        params.append(datetime.datetime.now())
        params.append(datetime.datetime.now())

        cur.execute(sql, params)
        self.conn.commit()

        return post_id

    def update(self, uid, data):
        """Update an article by it's id
        """

        if type(data) is not dict:
            raise TypeError('parameter `data` must be a dict object')

        params = []

        assert data['ext']
        assert data['ext'] == 'html'
        params.append(data['ext'])

        assert data['title'] and len(data['title']) > 0
        params.append(data['title'])

        assert data['source'] and len(data['source']) > 0
        params.append(data['source'])

        assert data['content'] and len(data['content']) > 0
        params.append(data['content'])

        if 'category' in data:
            category = data['category']
        else:
            category = config.app_settings['default_category']

        params.append(category)

        tags_str = ','.join(data['tags']) if 'tags' in data else ''
        params.append(','.join(['', tags_str, '']))

        params.append(data['state'])

        cur = self.conn.cursor()

        sql = """
              UPDATE posts
              SET ext = ?,
                  title = ?,
                  source = ?,
                  content = ?,
                  category = ?,
                  tags = ?,
                  state = ?,
                  updated_at = ?
              WHERE uuid = ?
              """
        params.append(datetime.datetime.now())
        params.append(uid)

        cur.execute(sql, params)
        self.conn.commit()

    def find(self, id_list=[], tag_list=[], limit=None, skip=0,
             before_date=None, after_date=None, states=[], categories=[]):

        id_list = filter(None, id_list)
        tag_list = filter(None, tag_list)
        states = filter(None, states)
        categories = filter(None, categories)

        sql = """
              SELECT

                  uuid,
                  ext,
                  title,
                  source,
                  content,
                  category,
                  tags,
                  state,
                  created_at as "created_at [timestamp]",
                  updated_at

              FROM posts WHERE 1
              """
        params = []

        if len(id_list) > 0:
            sql += " AND uuid IN (?) "
            params.append(','.join(id_list))

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

        if len(states) > 0:
            sql += " AND state IN (?)"
            params.append(','.join(states))

        if len(categories) > 0:
            sql += " AND category IN (?)"
            params.append(','.join(categories))

        sql += " ORDER BY created_at DESC"

        if limit:
            sql += " LIMIT ?"
            params.append(limit)

        if skip:
            sql += " OFFSET ?"
            params.append(skip)

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [self.__parse(self.to_dict(cur, p)) for p in cur.fetchall()]

    def count(self,
              tag_list=[],
              before_date=None,
              after_date=None,
              states=[],
              categories=[]):

        tag_list = filter(None, tag_list)
        states = filter(None, states)
        categories = filter(None, categories)

        sql = " SELECT count(*) as count FROM posts WHERE 1 "
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

        if len(states) > 0:
            sql += " AND state IN (?)"
            params.append(','.join(states))

        if len(categories) > 0:
            sql += " AND category IN (?)"
            params.append(','.join(categories))

        sql += " ORDER BY created_at DESC"

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()[0]

    def delete(self, uid):
        cur = self.conn.cursor()

        sql = """
              UPDATE posts
              SET state = ?,
                  updated_at = ?
              WHERE uuid = ?
              """
        params = ['deleted']
        params.append(datetime.datetime.now())
        params.append(uid)

        cur.execute(sql, params)
        self.conn.commit()

    def drop(self, uid):
        """Delete from trash. can't be recovered
        """

        cur = self.conn.cursor()

        sql = """
              DELETE FROM posts
              WHERE state = 'deleted'
              AND uuid = ?
              """
        params = [uid]

        cur.execute(sql, params)
        self.conn.commit()

    def find_posts_with_tag(self, tag):
        return self.find(tag_list=[tag])

    def find_posts_between_date(self, start_date, end_date):
        return self.find(
            states=['published'],
            before_date=end_date,
            after_date=start_date
        )

    def get_archives(self):
        """按创建日期给文章分组,
           并返回结构化的数据
        """
        posts = self.find(states=['published'])

        archives = {}
        for a in posts:
            year = a['created_at'].year
            month = a['created_at'].strftime('%m')
            month_abbr = calendar.month_abbr[a['created_at'].month]

            if year not in archives:
                archives[year] = {}

            if month not in archives[year]:
                archives[year][month] = {
                    'count': 0,
                    'abbr': month_abbr,
                    'posts': []
                }

            archives[year][month]['count'] += 1
            archives[year][month]['posts'].append(a)

        return archives

    def find_by_id(self, uuid):
        """Find an article by it's uuid
        """
        posts = self.find(id_list=[uuid])
        try:
            return posts[0]
        except IndexError:
            return None

    def find_by_category(self, cate):
        """Find posts with specific category"""
        return self.find(categories=[cate])

    def gen_uuid(self, title, content):
        """Generate post uuid based on it's content
        """

        m = hashlib.sha1()
        s = title + content + str(time.time())
        m.update(s.encode('utf-8'))
        uuid = m.hexdigest()[:8]
        return uuid

    def get_drafts(self):
        """Find all posts that are drafts.
        """
        return self.find(states=['draft'])

    def get_trash(self):
        """Find all posts that are deleted
        """
        return self.find(states=['deleted'])

    def find_published_posts(self):
        """Find all posts that are published."""
        return self.find(states=['published'])

    def find_published_posts_by_id(self, id_list):
        """Find all posts that are published."""
        return self.find(states=['published'])

    def get_posts(self):
        return self.find()

    def get_tags(self):
        """Find all tags availabilie
        """

        cur = self.conn.cursor()
        sql = """
        select tags from posts where state = 'published'
        """
        cur.execute(sql)
        article_tags = cur.fetchall()
        flat_tags_list = []

        for tags in article_tags:
            for t in tags[0].split(','):
                flat_tags_list.append(t)

        flat_tags_list = filter(None, [t.strip() for t in flat_tags_list])
        tags_count = {}
        for tag in flat_tags_list:
            if tag not in tags_count:
                tags_count[tag] = 0

            tags_count[tag] += 1

        result = []
        for tag, count in tags_count.items():
            result.append({
                'tag': tag,
                'count': count
            })

        return result
