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






class Member:
	# Required Properties
	uid = None
	role = None
	name = None
	name_safe = None
	email = None
	pwd = None 
	auth = None
	date = None
	avatar = None
	brief = None
	verified = False


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







