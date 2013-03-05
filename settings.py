#! /usr/bin/env python
# coding=utf-8

import os.path
import pymongo

# set True to turn on tornado debug mode. Default is True.
DEBUG = True

# tornado.web.Application configuration. static file settings
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
IMAGE_PATH = os.path.join(STATIC_PATH, 'img')

# tornado.web.Application configuration. template file settings
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')


ARTICLE_AVATAR_PATH = os.path.join(STATIC_PATH, IMAGE_PATH, 'article')


# article avatar is the image displayed on index page
DEFAULE_ARTICLE_AVATAR = "/static/img/article/intro-default.jpg"

# where to store log files
LOG_LOCATION = os.path.join(os.path.dirname(__file__), 'page302.log')

# MongoDB settings
DATABASE = pymongo.Connection('localhost',27017)['page302']

# default article category name
DEFAULT_CATEGORY = "default"

# default member role when first regist
ROLE = "author"
