#! /usr/bin/env python
# coding=utf-8
import time
import datetime

from settings import DATABASE
from settings import DEFAULE_ARTICLE_AVATAR

class Article:
    def __init__(self, db=DATABASE.article):
        self.db = db
        self.template = {
            '_id': str(int(time.time())),
            'status': 0, # 0 means normal
            'avatar': DEFAULE_ARTICLE_AVATAR,
            'author': None,
            'heat': 0, 
            'title': None,
            'brief': None,
            'body': None,
            'date': datetime.datetime.utcnow(),
            'review': datetime.datetime.utcnow(),
        }

    def set_author(self, uid):
        self.template['author'] = uid

    def set_title(self, title):
        self.template['title'] = title

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