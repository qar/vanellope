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

from vanellope.ext import db
from vanellope.model import Article
from vanellope.model import Comment
from vanellope.handlers import BaseHandler
from vanellope.handlers.comment import CommentHandler
from vanellope.handlers.member import MemberHandler
from vanellope.handlers.member import RegisterHandler
from vanellope.handlers.article import ArticleHandler
from vanellope.handlers.article import ArticleUpdateHandler

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver
from tornado.options import define, options

CSS_COlOR_PATT = r"#[0-9a-fA-F]{6}"

#class AjaxHandler(BaseHandler):
#    def post(self, func):
#        
#    
#    @tornado.web.authenticated
#    def change_color(self, color):  
#        master = self.get_current_user()
#        m = db.member.find_one({"uid": master['uid']})
#        m['color'] = color
#        db.member.save(m)
#        return True


class ColorHandler(BaseHandler):
    def post(self):
        color = self.get_argument("color", None)
        if re.match(CSS_COlOR_PATT, color):
            master = self.get_current_user()
            master['color'] = color
            db.member.save(master)
            return True
        else:
            return False



