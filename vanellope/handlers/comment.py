#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import datetime
from vanellope.handlers import BaseHandler
from vanellope import db


import tornado.web

class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, article_sn):
    	model = {
           'date': datetime.datetime.utcnow(),
           'article': None,
           'body': None,
           'member': None, 
           'floor': None,
        }

        master = self.get_current_user()
        try:
            cmt = self.get_argument('comment')
        except:
            self.redirect(self.request.headers['Referer'])

        if master:
            # basic commenter information
            commenter = {
                "uid": master['uid'],
                "name": master['name'],
                "name_safe": master['name_safe'],
                "avatar": master['avatar']
            }
            model['floor'] = db.comment.find({"article": int(article_sn)}).count() + 1
            model['article'] = int(article_sn)
            model['member'] = commenter
            model['body'] = cmt
            db.comment.insert(model)
            self.redirect("/article/%s" % article_sn)
        else:
            self.send_error(403)