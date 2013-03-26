#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import urlparse
import datetime
import smtplib
import string
import random
import json
import config

from vanellope import da
from vanellope import db, Mail
from urllib import quote_plus as url_escape

import tornado.web

EMAIL_PATT = r'^[-a-zA-Z0-9\.]+@[-a-zA-Z0-9]+\.[a-z]{2,4}$'
EMAIL_ERR = {
    # the dict key MUST NOT be changed
    'exist': u"This email address has being used",
    'invalid': u"It's not a valid email address",
}


class Member:
    def __init__(self):
        self._model = {
            'uid': da.total_member() + 1,
            'role': "reader",
            'name': None,
            'name_safe': None,
            'email': None,
            'pwd': None, 
            "color": None,
            'auth': None,
            'date': datetime.datetime.utcnow(),
            'avatar': None,
            'avatar_large': None,
            'brief': None,
            'verified': False,
        }
    
    def reload(self, auth=None):
        self._model = db.member.find_one({"auth":auth})
        return self._model

    # Required Properties
    def set_name(self, _name):
        # check uniqueness
        if db.member.find_one({"name": _name}):
            return False
        else:
            self._model['name'] = _name
            self._model['name_safe'] = _name.lower()
            self.set_auth()
            return True

    def set_password(self, _pwd):
        # raw password must be sha512() hashed
        if _pwd:
            hashed = hashlib.sha512(_pwd).hexdigest()
            self._model['pwd'] = hashed
            self.set_auth()
            return True
        else:
            return False

    def set_email(self, _email):
        # check
        print _email
        if re.match(EMAIL_PATT, _email.lower()):
            if db.member.find_one({"email": _email.lower()}):
                return False
            else:
                self._model['email'] = _email.lower() 
                return True
        else:
            return False

    def set_secret_key(self, _key):
        self._model['secret_key'] = _key

    def gravatar(self, email, size=64):
        gravatar_url = ("http://www.gravatar.com/avatar/%s" % hashlib.md5(email).hexdigest() + "?")
        gravatar_url += urllib.urlencode({'s':str(size)})
        return gravatar_url

    def verify(self):
        netloc = urlparse.urlsplit(config.HOSTNAME).netloc
        URL = "%s/verify/?" % (config.HOSTNAME,) + urllib.urlencode(
                                {"secret_key":self._model['secret_key']})
        SUBJECT = "[%s]邮件验证" % netloc
        CONTENT = '''
        <p>感谢您在 %s 注册, 点击下面的链接或将其复制到浏览器地址栏中打开进行最后的验证</p>
        <a href="%s">%s</a>
        ''' % (netloc, URL, URL)
        mail = Mail(Subject=SUBJECT, To=self._model['email'], Body=CONTENT)
        mail.Send()

    def set_auth(self):
        if self._model['name'] is not None and self._model['pwd'] is not None:
            self._model['auth'] = hashlib.sha512(self._model['name'] + self._model['pwd']).hexdigest()
        else:
            return False

    def get_auth(self):
        return self._model['auth']

    def put(self):
        self._model['avatar'] = self.gravatar(self._model['email'])
        self._model['avatar_large'] = self.gravatar(self._model['email'], size=128)
        db.member.insert(self._model)



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


class Article:
    def __init__(self):
        self._model = {
            'sn': None, # article numeric id
            'status': "normal", # 'deleted', 'normal',
            'author': None, #
            'heat': 0,
            'title': None,
            'sub_title': None,
            'markdown': None,
            'html': None,
            'date': datetime.datetime.utcnow(),
            'review': datetime.datetime.utcnow(),
            'permalink': None,
            'category': None,
        }

        # Set Serial Number.
        # Serial Number is integer number.
        # Serial Number maybe inconsistence if 
        #   there were articles ever being deleted from database
        # It always 1 bigger than the current biggest Serial Number
        if db.article.count() == 0:
            self._model['sn'] = 0;
        else:
            self._model['sn'] = db.article.find().sort("sn", -1)[0]['sn'] + 1

        #if kwargs:
        #    try:
        #        for k in model.keys():
        #            self.article[k] = kwargs[k]
        #    except:
        #        return False
        #else:
        #    self.article = self.model
    def set_title(self, _title):
        self._model['title'] = _title

    def set_sub_title(self, _sub_title):
        self._model['sub_title'] = _sub_title

    def set_markdown(self, _md):
        self._model['markdown'] = _md

    def set_html(self, _html):
        self._model['html'] = _html

    # as long as the _identifier is unique
    def set_author(self, _identifier):
        self._model['author'] = _identifier

    # save instance to database
    def put(self):
        db.article.save(self._model)

    def reload(self, _sn):
        self._model = db.article.find_one({"sn": int(_sn), "status":"normal"})
        return self._model
