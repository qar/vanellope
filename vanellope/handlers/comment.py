#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import datetime

import tornado.web

from vanellope import db
from vanellope.model import Comment 
from vanellope.handlers import BaseHandler



class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, article_sn):
        comment = Comment()
        m = Member(self.get_current_user()) # wrappered
        cmt = self.get_argument('comment', None)

        # basic commenter information
        commenter = {
            "uid": m.uid,
            "name": m.name,
            "avatar": m.avatar,
        }

        comment.set_article(int(article_sn))
        comment.set_commenter(commenter)
        comment.set_body(cmt)
        comment.put()
        self.redirect("/article/%s" % article_sn)
