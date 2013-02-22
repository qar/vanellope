#! /usr/bin/env python
# coding=utf-8

import os.path
import logging
from datetime import datetime
from page302.security import CheckAuth

import settings

ARTICLE_DEFAULT_AVATAR = os.path.join(settings.STATIC_PATH,
                         'img/article/intro-default.jpg')
DEFAULT_CATEGORY = 'default'

class Article():
    template = {
        'title': None,      
        'brief': None,      # article brief, only display on index page
        'category': DEFAULT_CATEGORY,   
        'sn':   None,       # article serial number
        'img': ARTICLE_DEFAULT_AVATAR,        # index page avatar
        'author': None,     # author id
        'heat': 0,       # reviewed times
        'statue':  None,    # 0=normal, 1=deleted, 
        'body': None,       # article main content
        'created_date': None,
        'review':None,      # latest modify date
    }

    def __init__(self):
        current_date = datetime.utcnow()
        member = CheckAuth()
        template['created_date'] = current_date
        template['created_date'] = current_date

    def set_title(self, title):
        template['title'] = title

    def set_brief(self, brief):
        template['brief'] = brief

    def set_category(self, category):
        template['category'] = category

    def set_sn(self, sn):
        template['sn'] = sn

    def set_author(auth_cookie):
        try:
            db_member = settings.DATABASE['member']
            member = CheckAuth(auth_cookie)
            template['author'] = member['author']
        except:
            logging.warning("Database Internal Error.")
    def 


        