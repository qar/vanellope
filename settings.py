#! /usr/bin/env python
# coding=utf-8

import os.path
import pymongo

DEBUG = True

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')

DATABASE = pymongo.Connection('localhost',27017)['page302']
