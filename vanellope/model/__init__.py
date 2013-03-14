#! /usr/bin/env python
# coding=utf-8

import re
import urllib
import hashlib
import datetime

from vanellope.ext import db

from urllib import quote_plus as url_escape

EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
EMAIL_ERR = {
    # the dict key MUST NOT be changed
    'exist': u"This email address has being used",
    'invalid': u"It's not a valid email address",
}

#class Member(object):
#    model = {
#        'uid': None,
#        'role': None,
#        'name': None,
#        'name_safe': None,
#        'email': None,
#        'pwd': None, 
#        'auth': None,
#        'date': None,
#        'avatar': None,
#        'brief': None,
#        'verified': False,
#    }
#
#    def __init__(self):
#        self.member = self.model
#    
#    # Required Properties
#    def name(self, _name):
#        # check uniqueness
#        if db.member.find_one({"name": _name}):
#            return False
#        else:
#            self.member['name'] = _name
#            return True
#
#    def password(self, _pwd):
#        # raw password must be sha512() hashed
#        if _pwd:
#            hashed = hashlib.sha512(_pwd).hexdigest()
#            self.member['pwd'] = hashed
#            return True
#        else:
#            return False
#
#    def email(self, _email):
#        # check uniqueness
#        if db.member.find_one({"email": _email.lower()}):
#            return False
#        else:
#            self.member['email'] = _email.lower()
#            return True
#
#
#    def __gravatar(self, email, size=128):
#        gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
#                        hashlib.md5(email.lower()).hexdigest() + "?")
#        gravatar_url += urllib.urlencode({'s':str(size)})
#        return gravatar_url
#
#    def get_auth(self):
#        return self.member['auth']
#
#
#    def put(self):
#        self.member['auth'] = hashlib.sha512(self.member['email'] + self.member['pwd']).hexdigest()
#        db.member.insert(self.member)



class Article(object):
    model = {
        'sn': None, # article numeric id
        'status': None, # 'deleted', 'normal',
        'avatar': None, # 
        'author': None, #
        'heat': None,
        'title': None,
        'sub_title': None,
        'body': None,
        'date': None,
        'review': None,
        'permalink': None,
        'category': None,
    }


    def __init__(self, **kwargs):
        if kwargs:
            try:
                for k in model.keys():
                    self.article[k] = kwargs[k]
            except:
                return False
        else:
            self.article = self.model


    # Required Properties

    def title(self, _title):
        self.article['title'] = _title

    def sub_title(self, _sub_title):
        self.article['sub_title'] = _sub_title

    def body(self, _body):
        self.article['body'] = _body

    def avatar(self, _avatar_link):
        self.article['avatar'] = _avatar_link

    # as long as the _identifier is unique
    def author(self, _identifier):
        self.article['author'] = _identifier

    # save instance to database
    def put(self):
        db.article.save(self.article)







class Comment:
    def __init__(self, date=None, article=None, body=None, member=None):
        self.comment = {
           'date': None,
           'article': None,
           'body': None,
           'member': None, 
        }

    def put(self):
        db.comment.insert(self.comment)


