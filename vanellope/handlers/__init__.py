#! /usr/bin/env python
# coding=utf-8

import tornado.web

from vanellope.ext import db

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        member = db.member.find_one({"auth": self.get_cookie('auth')})
        if member:
            return member
        else:
            return None

    