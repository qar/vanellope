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

class WidgetsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, w=None):
        path = os.path.join(self.application.settings['template_path'],'widgets',w)
        if os.path.exists(path):
            f = open(path, 'r')
            self.finish(f.read())
        else:
            self.send_error(404)
            self.finish()
            
class ColorHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        color = self.get_argument("color", None)
        master = self.current_user_entity() #wrapped
        try:
            master.set_color(color)
            master.put()
            master.color
            self.finish(json.dumps([])) # a empty array indicate no error occors
        except exception.PatternMatchError:
            errors = u"不支持的CSS颜色属性"
            self.finish(json.dumps(errors))


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



class ExportHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_sn=None):
        # Export one single article or a bunch of articles
        current_user = self.get_current_user()
        if article_sn:
            chunk = da.get_article_by_sn(int(article_sn))
            if chunk['author'] == current_user['uid']:
                chunk['date'] = (chunk['date'] + 
                           datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") 
                chunk['review'] = (chunk['review'] + 
                           datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
                del chunk['_id'] 
                self.finish(chunk)     
            else:
                self.send_error(403)       
