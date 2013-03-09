#! /usr/bin/env python
# coding=utf-8

import re
import urllib
import hashlib
import datetime
from settings import DATABASE, ROLE

from urllib import quote_plus as url_escape

def CheckAuth(auth_cookie):
    # take a cookie name that do authentication function
    db_member = DATABASE['member']
    member = db_member.find_one({"auth": auth_cookie})
    if member:
        return member
    else:
        return None

def Avatar(email, size=128):
    # Using Gravatar
    LARGE = 128
    gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
                    hashlib.md5(email.lower()).hexdigest() + "?")
    # use local default avatar
    #gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    #default = "static/img/avatar/default.png"

    # use gravatar default img
    gravatar_url += urllib.urlencode({'s':str(size)})
    return gravatar_url

class Member:
    def __init__(self, db=DATABASE.member ):
        self.db = db
        self.member = {
            "role": ROLE,
            "verified":False,
            "date": datetime.datetime.utcnow(),
        }

    def check_name(self, name):
        # check user input name's usability
        errors = []
        UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
        if re.match(UID_PATT, name):
            if self.db.find_one({"name": name}):
                errors.append("uname exist")
            else:
                self.member['name'] = name
                self.member['name_safe'] = url_escape(name.lower())
        else:
            errors.append("illegal character")
        return errors

    def set_pwd(self, pwd):
        # authentication password
        self.member['pwd'] = hashlib.sha512(pwd).hexdigest()

    def check_email(self, email):
        # check whether the given email is being using
        # authentication email
        EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
        errors = []
        if re.match(EMAIL_PATT, email.lower()):
            if self.db.find_one({"email": email.lower()}):
                errors.append("email already being used")
            else:
                self.member['email'] = email.lower()
                self.member['avatar'] = Avatar(self.member['email'])
                self.member['uid'] = hashlib.md5(email.lower()).hexdigest()
        else:
            errors.append("illegal email address")
        return errors

    def __set_auth(self):
        auth = hashlib.sha512(self.member['name']+self.member['pwd']).hexdigest()
        self.member['auth'] = auth

    def get_auth(self):
        return self.member['auth']

    def save(self):
         # the tuple below are the other part of necessary items' keys
        self.__set_auth()
        keys = ('name', 'name_safe', 'pwd', 'email', 'auth', 'avatar', 'uid')
        if len([x for x in keys if x in self.member.keys()]) == len(keys):
            self.db.insert(self.member)
            return True
        else:
            return False







    

