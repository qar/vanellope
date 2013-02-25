#! /usr/bin/env python
# coding=utf-8

import os.path
import logging
import time
import settings

from datetime import datetime
from page302.security import CheckAuth

class Article():
    def __init__(self):
        self.template = { 
        'sn':  str(int(time.time())),
        'statue': 0,
        'img': None,
        'author': None,
        'heat': 0,
        'title': None,
        'brief': None,
        'body': None,
        'date': datetime.utcnow(),
        'review': datetime.utcnow(),
    }
        self.db = settings.DATABASE['article']

    def get_author_all_articles(self, member_id):
        articles = self.db.find({"author_id": member_id}).sort("date", -1)
        return articles



        