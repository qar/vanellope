#! /usr/bin/env python
# coding=utf-8

import os.path
import logging
import time
import settings

from datetime import datetime
from page302.security import CheckAuth

class Article():
    template = { 
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
    def __init__(self):
        self = template