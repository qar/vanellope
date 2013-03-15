#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import datetime

from vanellope.ext import db
from vanellope.handlers import BaseHandler

import tornado.web

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", title="Login", errors=None, master=False)

    def post(self):
        template = "login.html"
        errors = []
        
        post_values = ['name','pwd']
        args = {}
        try:
            for v in post_values:
                args[v] = self.get_argument(v)
        except:
            errors.append("complete the blanks")
            self.render(template, 
                        title="Login", 
                        master=False, 
                        errors=errors)
        try:
            member = db.member.find_one({'name':args['name']})
            input_auth = hashlib.sha512(args['name'] + 
                        hashlib.sha512(args['pwd']).hexdigest()).hexdigest()
        except:
            errors.append("db error")
            self.render(template, 
                        title = "Login",
                        master = False, 
                        errors = errors)

        if member and (member['auth'] == input_auth):
            self.set_cookie(name = "auth", 
                            value = member['auth'], 
                            expires_days = 365)
            self.redirect('/')
        else:
            errors.append("error with user name or password") 
            self.render(template, 
                        title = "Login", 
                        master = False, 
                        errors = errors)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')
                    