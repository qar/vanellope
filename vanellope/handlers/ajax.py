#! /usr/bin/env python
# coding=utf-8

import os
import sys
import os.path
import hashlib
import datetime
import time
import logging
import re
import pymongo
import markdown

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from vanellope import db
from vanellope import Mail
from vanellope import regex

from vanellope.handlers import BaseHandler


class ColorHandler(BaseHandler):
    def post(self):
        color = self.get_argument("color", None)
        if re.match(regex.COLOR, color):
            master = self.get_current_user()
            master['color'] = color
            db.member.save(master)
            return True
        else:
            return False



