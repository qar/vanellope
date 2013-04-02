#! /usr/bin/env python
# coding=utf-8

import re
import time
import hashlib
import urllib
import urlparse
import datetime
import smtplib
import string
import random
import json
import config
import logging

from urllib import quote_plus as url_escape

import tornado.web

from vanellope import db
from vanellope import Mail
from vanellope import regex
from vanellope import constant as cst
from vanellope import exception 

"""Database Schema
"""

class Member:
    """A wrapper.

    set_name() takes a string as argument. ValueError exception raised if the 
    string's boolean value if False. PatternMatchError exception is raised 
    if the string did not match the regex pattern. AuthError exception is 
    raised if the name was taken.
    """
    def __init__(self, entity=None):
        self._model = {
            'uid': None,
            'name': None,
            'email': None,
            'pwd': None, 
            "color": None,
            'auth': None,
            'date': datetime.datetime.utcnow(),
            'avatar': None,
            'avatar_large': None,
            'brief': None,
            'like': [],
            'verified': False,
        }
        
        if entity and isinstance(entity, dict):
            self._model = entity

    # Is is NECESSARY ???????
    def __getitem__(self, item):
        try:
            return self._model[item]
        except KeyError:
            return None

    @property 
    def uid(self):
        return self._model['uid']

    @property 
    def name(self):
        return self._model['name']

    @property 
    def email(self):
        return self._model['email']

    @property 
    def color(self):
        return self._model['color']

    @property 
    def brief(self):
        return self._model['brief']

    @property 
    def avatar_large(self):
        return self._model['avatar_large']

    @property 
    def avatar(self):
        return self._model['avatar']

    @property
    def auth(self):
        return self._model['auth']

    @property 
    def secret_key(self):
        if self._model.has_key("secret_key"):
            return self._model['secret_key']
        else:
            return None
        
    @property
    def verified(self):
        return self._model['verified'] # True or False

    @property 
    def pack(self):
        return self._model

    # Required Properties
    def set_name(self, _name):
        self._model['uid'] = db.member.count() + 1
        if not _name:
            raise exception.NameError
        elif re.match(regex.UNAME, _name):
            if db.member.find_one({"name": _name}):
                raise exception.DupKeyError()
            else:
                self._model['name'] = _name
                self._model['name_safe'] = _name.lower()
                self._set_auth()
        else:
            raise exception.PatternMatchError()

    def set_color(self, color):
        if re.match(regex.COLOR, color):
            self._model['color'] = color
        else:
            raise exception.PatternMatchError()


    def set_password(self, _pwd):
        # _pwd is inscure. 
        # If _pwd is not string, TypeError (from method _encrypt_password)
        # raised.
        self._model['pwd'] = self._encrypt_password(_pwd)
        self._set_auth()

    def set_brief(self, _brief):
        self._model['brief'] = _brief

    def set_email(self, _email):
        # check
        if _email is None:
            raise ValueError
        elif re.match(regex.EMAIL, _email.lower()):
            if db.member.find_one({"email": _email.lower()}):
                raise exception.DupKeyError()
            else:
                self._model['email'] = _email.lower() 
                self._model['verified'] = False # new email need be verified
        else:
            raise exception.PatternMatchError()

    def like(self, article):
        if int(article) not in self._model['like']:
            self._model['like'].append(int(article))
        else:
            self._model['like'].remove(int(article))
       

    def check_password(self, _pwd):
        #
        # Given a raw password, compare the generated hashed password 
        # and self._model['pwd']
        #
        try:
            if self._encrypt_password(_pwd) == self._model['pwd']:
                return True
            else:
                return False
        except TypeError:
            return False


    def set_secret_key(self, _key):
        self._model['secret_key'] = _key

    def gravatar(self, email, size=64):
        gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
                        hashlib.md5(email).hexdigest() + "?")
        gravatar_url += urllib.urlencode({'s':str(size)})
        return gravatar_url

    def verify(self):
        netloc = urlparse.urlsplit(config.HOSTNAME).netloc
        URL = "%s/verify?" % (config.HOSTNAME,) + urllib.urlencode(
                                {"key":self._model['secret_key']})
        SUBJECT = "[%s]邮件验证" % netloc
        CONTENT = '''
        <p>感谢您在 %s 注册, 点击下面的链接或将其复制到浏览器地址栏中打开进行最后的验证</p>
        <a href="%s">%s</a>
        ''' % (netloc, URL, URL)
        mail = Mail(Subject=SUBJECT, To=self._model['email'], Body=CONTENT)
        mail.Send()

    def getverified(self):
        self._model['verified'] = True

    def _encrypt_password(self, _pwd):
        # Unified password encryption algorithm
        return hashlib.sha256(_pwd).hexdigest()

    def _set_auth(self):
        if self._model['name'] and self._model['pwd']:
            self._model['auth'] = hashlib.sha256(self._model['name'] + 
                                  self._model['pwd']).hexdigest()

    def reload(self, _name, _pwd):
        """
        Take username and password as argument. Position matters.
        ValueError exception is raised when username's boolean value is False.
        If password is not match, AuthError exception is raised.
        More about AuthError exception see  'vanellope/exception.py'.
        """
        # Use (name, pwd) pair or auth cookie to reload
        if not _name:
            raise exception.NameError
        elif not _pwd:
            raise exception.AuthError()
        else:
            entity = db.member.find_one({"name": _name})
            # Pymongo return None value if not match one
            if not entity:
                raise exception.AuthError()
            elif entity['pwd'] != self._encrypt_password(_pwd):
                raise exception.AuthError()
            else:
                self._model = entity

    def put(self):
        self._model['avatar'] = self.gravatar(self._model['email'])
        self._model['avatar_large'] = self.gravatar(self._model['email'], size=128)
        db.member.save(self._model)






class Comment:
    def __init__(self, entity=None):
        self._model = {
           'cid': None, 
           'date': datetime.datetime.utcnow(),
           'article': None,
           'body': None,
           'member': None,
        }
        if entity and isinstance(entity, dict):
            self._model = entity

    @property 
    def cid(self):
        return self._model['cid']

    @property 
    def member(self):
        return self._model['member']

    @property 
    def body(self):
        return self._model['body']

    @property 
    def date(self):
        return self._model['date']

    def set_article(self, _sn):
        self._model['article'] = int(_sn)
        self._model['cid'] = db.comment.find({"article":int(_sn)}).count() + 1

    def set_body(self, _body):
        self._model['body'] = _body


    def set_commenter(self, _uid):
        self._model['member'] = _uid

    def put(self):
        db.comment.save(self._model)



class Article:
    def __init__(self, entity=None):
        self._model = {
            'sn': None, # article numeric id
            'status': cst.NORMAL, # 'deleted', 'normal',
            'author': None, #
            'heat': 0,
            'title': None,
            'sub_title': None,
            'markdown': None,
            'html': None,
            'date': datetime.datetime.utcnow(),
            'review': datetime.datetime.utcnow(),
            'permalink': None,
        }

        if entity and isinstance(entity, dict):
            self._model = entity

    @property 
    def status(self):
        return self._model['status']

    @property 
    def sn(self):
        # Whatever it calls, sn refer to the numeric id.
        return self._model['sn']

    @property 
    def author(self):
        return self._model['author']

    @property 
    def title(self):
        return self._model['title']

    @property 
    def sub_title(self):
        return self._model['sub_title']

    @property 
    def html(self):
        return self._model['html']

    @property 
    def markdown(self):
        return self._model['markdown']

    @property 
    def date(self):
        return self._model['date']

    @property 
    def review(self):
        return self._model['review']

    @property 
    def heat(self):
        return self._model['heat']

    def set_sn(self):
        if db.article.count() == 0:
            self._model['sn'] = 0;
        else:
            self._model['sn'] = db.article.find().sort("sn", -1)[0]['sn'] + 1

    def set_title(self, _title):
        self._model['title'] = _title

    def set_sub_title(self, _sub_title):
        self._model['sub_title'] = _sub_title

    def set_markdown(self, _md):
        self._model['markdown'] = _md

    def set_html(self, _html):
        self._model['html'] = _html

    def set_status(self, _status):
        self._model['status'] = _status

    # as long as the _identifier is unique
    def set_author(self, _identifier):
        self._model['author'] = _identifier

    def set_review(self):
        self._model['review'] = datetime.datetime.utcnow()

    def remove(self):
        db.article.remove({"sn": self._model['sn']})

    # save instance to database
    def put(self):
        db.article.save(self._model)



class Message:
    def __init__(self, entity=None):
        self._model = {
            "mid": None, #mid只能用来标识确定两个用户之间的信息
            "uid": None, # Unique among all messages
            "sender": None, 
            "receiver": None,
            "reject": False,
            "status": cst.UNREAD,
            "date": datetime.datetime.utcnow(),
            "body": None,
            "peer": [], # the two contacters' uid.
        }

        if entity:
            self._model = entity

    # Access like attribute
    
    @property 
    def mid(self):
        return self._model['mid']

    @property 
    def sender(self):
        return self._model['sender']

    @property 
    def receiver(self):
        return self._model['receiver']

    @property 
    def reject(self):
        return self._model['reject']

    @property 
    def status(self):
        return self._model['status']

    @property 
    def date(self):
        return self._model['date']

    @property 
    def body(self):
        return self._model['body']

    @property 
    def peer(self):
        return self._model['peer']
        


    # Utilities
    def set_sender(self, sender_id):
        if not isinstance(sender_id, int): # invalid argument
            raise TypeError
        else:
            self._model['sender'] = sender_id
            self._model['peer'].append(sender_id)

    def set_receiver(self, receiver_id):
        if not isinstance(receiver_id, int): # invalid argument
            raise TypeError
        else:
            self._model['receiver'] = receiver_id
            self._model['peer'].append(receiver_id)

    def set_body(self, msg):
        if not msg: # content empty
            raise ValueError
        else:
            self._model['body'] = msg

    def set_reject(self):
        self._model['reject'] = True


    def put(self):
        t = db.message.find({"sender": self._model['sender'],
                             "receiver": self._model['receiver']}).count()
        self._model['mid'] = t + 1
        self._model['uid'] = int(time.time())
        db.message.save(self._model)

    def drop(self):
        db.message.remove({"uid": self._model['uid']})

