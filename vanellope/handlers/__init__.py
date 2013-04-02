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
            return dict(
                uid = member['uid'],
                name = member['name'],
                email = member['email'],
                color = member['color'],            
                brief = member['brief'],
                like = member['like'],
                avatar = member['avatar'],
                avatar_large = member['avatar_large'],
                messages = da.unread_messages(member['uid']),
                verified = member['verified'],
            )
        else:
            return None

    def get_user(self, uid=None, name=None):
        if uid:
            member = db.member.find_one({"uid":int(uid)})
        elif name:
            member = db.member.find_one({"name": name})
        else: 
            return None
        if member:
            return dict(
                uid = member['uid'],
                name = member['name'],
                email = member['email'],
                color = member['color'],            
                brief = member['brief'],
                like = member['like'],
                avatar = member['avatar'],
                avatar_large = member['avatar_large'],
                messages = da.unread_messages(member['uid']),
                verified = member['verified'],
            )


    def current_user_entity(self):
        # For write
        return Member(db.member.find_one({"auth": self.get_cookie('auth')}))

    def user_entity(self, uid=None, name=None):
        if uid:
            return Member(db.member.find_one({"uid":int(uid)}))
        elif name:
            return Member(db.member.find_one({"name": name}))

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



