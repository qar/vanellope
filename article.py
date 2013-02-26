#! /usr/bin/env python
# coding=utf-8
import time
import datetime
import tornado.escape

from settings import DATABASE
from settings import DEFAULE_ARTICLE_AVATAR

class Article:
    def __init__(self, db=DATABASE.article):
        self.db = db
        self.template = {
            'sn': self.set_id(),
            'status': 0, # 0 means normal
            'avatar': DEFAULE_ARTICLE_AVATAR,
            'author': None,
            'heat': 0, 
            'title': None,
            'brief': None,
            'body': None,
            'date': datetime.datetime.utcnow(),
            'review': datetime.datetime.utcnow(),
            'permalink': None,
        }

    def set_id(self):
        #set article unique id.
        #id is a unique number. it's one bigger than 
        # the biggest article id in the article database.
        # When member deleted some articles they owned, 
        #  the id may be inconsistent, but it's okay

        try:
            biggest = self.db.find_one({}).sort("_id, -1")[0]['_id']
            return biggest+1
        except:
            # 0 is initial article id
            return 0

    def gen_permalink(self, title):
        self.template['permalink'] = '_'.join(
            (str(self.template['sn']),tornado.escape.url_escape(title)))

    def set_author(self, uid):
        self.template['author'] = uid

    def set_title(self, title):
        self.template['title'] = title
        self.gen_permalink(title)

    def set_brief(self, brief):
        self.template['brief'] = brief

    def set_content(self, content):
        self.template['body'] = content

    def set_avatar(self, fp):
        self.template['img'] = fp

    def save(self):
        self.db.insert(self.template)

    #def fetch_by_id(self, )

    def find_one(self):
        print self.db.find_one()


if __name__ == "__main__":
    article = Article()
    print article.find_one()
    print article.template