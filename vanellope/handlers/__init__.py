#! /usr/bin/env python
# coding=utf-8

import tornado.web

from vanellope import da
from vanellope import db

from vanellope.model import Member

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        member = db.member.find_one({"auth": self.get_cookie('auth')})
        if member:
            return member
        else:
            return None

    def master(self):
        # get template values
        m = Member(self.get_current_user())
        return dict(
            uid = m.uid,
            color = m.color,            
            avatar_large = m.avatar_large,
            avatar = m.avatar,
            brief = m.brief,
            name = m.name,
            email = m.email,
            like = m.likeit,
            messages = da.unread_messages(m.uid)
        )

    def member(self, uid):
        m = Member(da.get_member_by_uid(int(uid)))
        return dict(
            uid = m.uid,
            color = m.color,            
            avatar_large = m.avatar_large,
            avatar = m.avatar,
            brief = m.brief,
            name = m.name,
            email = m.email,
        )
        
    def is_ajax(self):
        return "X-Requested-With" in self.request.headers and \
            self.request.headers['X-Requested-With'] == "XMLHttpRequest"



