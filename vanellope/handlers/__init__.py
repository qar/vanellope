#! /usr/bin/env python
# coding=utf-8

import tornado.web

from vanellope import da
from vanellope import db

from vanellope.model import Member

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # For read only
        member = db.member.find_one({"auth": self.get_cookie('auth')})
        if member:
            return self._member_db_map(member)
        else:
            return {}

    def get_user(self, uid=None, name=None):
        if uid:
            return self._member_db_map(db.member.find_one({"uid":int(uid)}))
        elif name:
            return self._member_db_map(db.member.find_one({"name": name}))
        else: 
            return {}

    def current_user_entity(self):
        # For write
        return Member(db.member.find_one({"auth": self.get_cookie('auth')}))

    def user_entity(self, uid=None, name=None):
        if uid:
            return Member(db.member.find_one({"uid":int(uid)}))
        elif name:
            return Member(db.member.find_one({"name": name}))

    def member(self, uid):
        return self._member_db_map(db.member.find_one({"uid": int(uid)}))
        
    def is_ajax(self):
        return "X-Requested-With" in self.request.headers and \
            self.request.headers['X-Requested-With'] == "XMLHttpRequest"

    def _member_db_map(self, db):
        # The returned dict object supply a uniform database access interface 
        try:
            return dict(
                uid = db['uid'],
                name = db['name'],
                email = db['email'],
                color = db['color'],            
                brief = db['brief'],
                like = db['like'],
                avatar = db['avatar'],
                avatar_large = db['avatar_large'],
                messages = da.unread_messages(db['uid']),
                verified = db['verified'],
                contacter = db['contacter']
            )
        except TypeError:
            return {}



