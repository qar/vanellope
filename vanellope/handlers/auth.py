#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import datetime
import smtplib
import random
from email.mime.text import MIMEText

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
                    
class ForgetHandler(BaseHandler):
    def get(self):
        self.render("forget.html", title="Login", errors=None, master=False)

    def post(self):
        errors = []

        name = self.get_argument("name")
        email = self.get_argument("email")

        member = db.member.find_one({"name": name})
        if member:
            if email == member['email']:
                secure_key = hashlib.md5(email + str(random.random())).hexdigest()
                member['secure_key']  = secure_key
                db.member.save(member)
                FROM = "no-reply@page302.com"
                TO = email
                CONTENT = """
                    <h1>click the link to change your password</h1>
                    <a href="localhost:8000/password?key=%s">localhost:8000/password?key=%s</a>
                """ % (secure_key, secure_key)
                msg = MIMEText(CONTENT, 'html')
                msg['Subject'] = "[page302.com] Change password"
                msg['From'] = FROM
                msg['To'] = TO
                s = smtplib.SMTP('smtp.exmail.qq.com:25')
                s.login("no-reply@page302.com", "abs&qar.45")
                s.sendmail(FROM, [TO], msg.as_string())
                s.quit()
                self.redirect("/")
            else:
                errors.append(u"email is wrong")
                self.render("forget.html", 
                        title = "forget", 
                        master = False, 
                        errors = errors)
        else:
            errors.append(u"no such user")
            self.render("forget.html", 
                        title = "forget", 
                        master = False, 
                        errors = errors)

class PasswordHandler(BaseHandler):
    def get(self):
        secure_key = self.get_argument("key")
        member = db.member.find_one({"secure_key": secure_key})
        if member:
            self.render("password.html", title="Change Password", errors=None, master=False, key=secure_key)
        else:
            self.send_error(404)
            self.finish()

    def post(self):
        errors = []
        pwd = self.get_argument("pwd")
        cpwd = self.get_argument("cpwd")
        secure_key = self.get_argument("key")

        member = db.member.find_one({"secure_key": secure_key})
        if member:
            if pwd == cpwd:
                member['pwd'] = hashlib.sha512(pwd).hexdigest()
                member['auth'] = hashlib.sha512(member['name'] + member['pwd']).hexdigest()
                del member['secure_key']
                db.member.save(member)
                self.set_cookie(name = "auth", 
                            value = member['auth'], 
                            expires_days = 365)
                self.redirect('/')

            else:
                errors.append(u"different password")
                self.render("password.html", 
                        title = "Change Password", 
                        master = False, 
                        errors = errors)
        else:
            errors.append(u"invalid secure link")
            self.render("password.html", 
                        title = "Change Password", 
                        master = False, 
                        errors = errors)



    


        


            
