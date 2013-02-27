#! /usr/bin/env python
# coding=utf-8

import hashlib
import settings
import datetime
import tornado.escape

class Member:
    def __init__(self, db=settings.DATABASE.member):
        self.db = db
        self.template = {
            "uid": None, # set this when setting email
            "role": 1,
            "name": None,
            "name_safe": None,
            "email": None, # set email along with uid
            "pwd": None,
            "auth": None,
            "date": None,
            "avatar": None,
        }
    def check_name(self, name):
        # check whether user with given 'name' already exists.
        result = self.db.find_one({"name": name})
        if result:
            return True
        else:
            return False

    def check_email(self, email):
        # check whether the given email is being using
        result = self.db.find_one({"email": email.lower()})
        if result:
            return True
        else:
            return False

    def set_name(self, name):
        self.template['name'] = name
        self.template['name_safe'] = tornado.escape.url_escape(name.lower())

    def set_pwd(self, hashed_pwd):
        self.template['pwd'] = hashed_pwd

    def set_email(self, email):
        self.template['email'] = email.lower()
        self.template['uid'] = hashlib.md5(email.lower()).hexdigest()

    def set_avatar(self, avatar_link):
        self.template['avatar'] = avatar_link

    def set_auth(self, auth):
        self.template['auth'] = auth

    def save(self):
        self.template['date'] = datetime.datetime.utcnow()
        self.db.insert(self.template)






    

