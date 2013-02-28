#! /usr/bin/env python
# coding=utf-8

import os.path
import pymongo


DEBUG = True

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

IMAGE_PATH = os.path.join(STATIC_PATH, 'img')

ARTICLE_AVATAR_PATH = os.path.join(STATIC_PATH, IMAGE_PATH, 'article')

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')

# article avatar is the image displayed on index page
DEFAULE_ARTICLE_AVATAR = "/static/img/article/intro-default.jpg"

# where to store log files
LOG_LOCATION = os.path.join(os.path.dirname(__file__), 'page302.log')

# MongoDB
DATABASE = pymongo.Connection('localhost',27017)['page302']

# default article category name
DEFAULT_CATEGORY = "default"

# default member role when first regist
ROLE = "author"
