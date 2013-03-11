#! /usr/bin/env python
# coding=utf-8

import os.path
import pymongo


ARTICLE_AVATAR_PATH = os.path.join(STATIC_PATH, IMAGE_PATH, 'article')


# article avatar is the image displayed on index page
DEFAULE_ARTICLE_AVATAR = "/static/img/article/intro-default.jpg"

# MongoDB settings
DATABASE = pymongo.Connection('localhost',27017)['page302']

# default article category name
DEFAULT_CATEGORY = "default"

# default member role when first regist
ROLE = "author"
