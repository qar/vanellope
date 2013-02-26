#! /usr/bin/env python
# coding=utf-8

import os.path
import pymongo


DEBUG = True

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

IMAGE_PATH = os.path.join(STATIC_PATH, 'img')

ARTICLE_AVATAR_PATH = os.path.join(STATIC_PATH, IMAGE_PATH, 'article')

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')

DATABASE = pymongo.Connection('localhost',27017)['page302']

DEFAULE_ARTICLE_AVATAR = "/static/img/article/intro-default.jpg"

LOG_LOCATION = os.path.join(os.path.dirname(__file__), 'page302.log')
