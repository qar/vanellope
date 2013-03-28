#! /usr/bin/env python
# coding=utf-8

import tornado.web

from vanellope import db
from vanellope.model import Member

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        member = db.member.find_one({"auth": self.get_cookie('auth')})
        if member:
            return member
        else:
            return None

