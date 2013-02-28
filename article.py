#! /usr/bin/env python
# coding=utf-8
import time
import datetime
from urllib import quote_plus as url_escape
from settings import DATABASE
from settings import DEFAULT_CATEGORY
from settings import DEFAULE_ARTICLE_AVATAR

class Article:
    def __init__(self, db=DATABASE.article):
        self.db = db
        self.article = {
        # These are part of necessary items.
            'sn': self.__new_sn(),
            'status': "normal",
            'heat': 0, 
            'avatar': DEFAULE_ARTICLE_AVATAR,
            'category':DEFAULT_CATEGORY,
            'date': datetime.datetime.utcnow(),
            'review': datetime.datetime.utcnow(),
        }

    def __new_sn(self):
        # set article serial number.
        # Serial Number(sn) is unique, ascending number.
        # Roughly it's the generated sequence of articles. It will make it 
        #  discontinuous if there were articles being deleted.
        try:
            # Find the biggest sn number in the database  and 
            # the new sn number should be ONE biggest than that.
            return self.db.find().sort("sn", -1)[0]['sn'] + 1
        except:
            # 0 is initial article sn number.
            return 0

    # methods called outside
    def set_title(self, title):
        # set title and permalink
        self.article['title'] = title
        self.article['permalink'] = '_'.join(
            (str(self.article['sn']), url_escape(title)))

    def set_author(self, uid):
        self.article['author'] = uid

    def set_brief(self, brief):
        self.article['brief'] = brief

    def set_content(self, content):
        self.article['body'] = content

    def set_avatar(self, fp):
        self.article['avatar'] = fp

    def save(self):
        # the tuple below are the other part of necessary items' keys
        keys = ('author', 'title', 'body', 'brief', 'permalink')
        if len([x for x in keys if x in self.article.keys()]) == len(keys):
            self.db.insert(self.article)
            return True
        else:
            return False

    # readOnly methods
    def find_adjoins(self, current_date):
        try:
            pre = db.find({"status":"normal",
                          "date": {"$lt": current_date}
                          }).sort("date",-1)[0]['sn']
        except:
            pre = None
        try:
            fol = db.find({"status":"normal",
                           "date": {"$gt": current_date}
                           }).sort("date", 1)[0]['sn']
        except:
            fol = None
        return (pre, fol)
