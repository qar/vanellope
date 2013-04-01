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
import json
import pymongo
import markdown

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from vanellope import da
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


class LikeHandler(BaseHandler):
    def get(self):
        article_sn = self.get_argument("article", None)
        total_like = da.article_total_like(int(article_sn))
        current_user = self.get_current_user()
        if current_user and (int(article_sn) in current_user['like']):
            i_like = True
        else:
            i_like = False
        self.finish(json.dumps([i_like, total_like]))

    @tornado.web.authenticated
    def post(self):
        article_sn = self.get_argument("article", None)
        master = self.current_user_entity()

        try:
            master.like(int(article_sn))
        except:
            pass

        master.put()
        total_like = da.article_total_like(int(article_sn))
        self.finish(json.dumps([True, total_like]))

