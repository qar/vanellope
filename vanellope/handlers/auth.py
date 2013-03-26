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


import tornado.web

from vanellope import da
from vanellope.ext import db, Mail
from vanellope.handlers import BaseHandler

UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
EMAIL_ERR = {
    # the dict key MUST NOT be changed
    'exist': u"This email address has being used",
    'invalid': u"It's not a valid email address",
}


CSS_COlOR_PATT = r"#[0-9a-fA-F]{6}"

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", 
                    title = 'Register',
                    errors = None,
                    master = None)

    @tornado.web.asynchronous
    def post(self):
        model = {
            'uid': None,
            'role': "reader",
            'name': None,
            'name_safe': None,
            'email': None,
            'pwd': None, 
            "color": None,
            'auth': None,
            'date': datetime.datetime.utcnow(),
            'avatar': None,
            'brief': None,
            'verified': False,
        }
        errors = []
        post_values = ['name','pwd','cpwd','email']
        args = {}
        for v in post_values:
            args[v] = self.get_argument(v, None)
            if args[v] is None:
                errors.append("complete the blanks")
                self.render("register.html",
                            title="Register",
                            master = None,
                            errors=errors)

        # set user name
        # check user input name's usability
        if re.match(UID_PATT, args['name']):
            if da.get_member_by_name(args['name']):
                errors.append(u"user name has being taken")
            else:
                model['name'] = args['name']
                model['name_safe'] = args['name'].lower()
        else:
            errors.append(u"illegal character")

        # set user password
        if args['pwd'] and (args['pwd'] == args['cpwd']):
            hashed = hashlib.sha512(args['pwd']).hexdigest()
            model['pwd'] = hashed
        else:
            errors.append(u"password different")

        # set user email
        if args['email'] and re.match(EMAIL_PATT, args['email'].lower()):
            if get_member_by_email_lower(args['email'].lower()):
                errors.append(u"This email address has being used")
            else:
                model['email'] = args['email']
        else:
            errors.append(u"It's not a valid email address")

        if errors:
            self.render("register.html", #template file
                        title = "Register", # web page title
                        errors = errors,    
                        master = None)
        else:
            model['uid'] = da.total_member() + 1
            model['date'] = datetime.datetime.utcnow()
            model['auth'] = hashlib.sha512(model['name'] + model['pwd']).hexdigest()
            gravatar = ("http://www.gravatar.com/avatar/%s" % 
                             hashlib.md5(model['email']).hexdigest() + "?")
            model['avatar'] = gravatar + urllib.urlencode({'s':64})
            model['avatar_large'] = gravatar + urllib.urlencode({'s':128})
            model['secret_key'] = randomwords(20)
            da.insert_new_member(model)
            netloc = urlparse.urlsplit(config.HOSTNAME).netloc
            URL = "%s/verify/?" % (config.HOSTNAME,) + urllib.urlencode(
                                {"secret_key":model['secret_key']})
            SUBJECT = "[%s]邮件验证" % netloc
            CONTENT = '''
            <p>感谢您在 %s 注册, 点击下面的链接或将其复制到浏览器地址栏中打开进行最后的验证</p>
            <a href="%s">%s</a>
            ''' % (netloc, URL, URL)
            mail = Mail(Subject=SUBJECT, To=model['email'], Body=CONTENT)
            mail.Send()

            self.set_cookie(name="auth", 
                            value=model['auth'], 
                            expires_days = 365)
            self.redirect('/')


class VerifyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = self.get_argument("name", None)
        secret_key = self.get_argument("secret_key", None)
        master = self.get_current_user()
        if master['verified'] == False:
            if secret_key == master['secret_key']:
                master['verified'] = True
                del master['secret_key']
                da.save_member(master)
                self.write("your email is activated\n") # everything fine
            else:
                self.write("url invalid") # url insecure
        else:
            self.write("your email has been activated already") # email has been verified
        self.finish()

class PasswordResetHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):        
        #
        # user intend to change password.
        # origin password is required to prevent malicious option.
        #
        errors = []
        args = dict(
            origin_pwd = self.get_argument("originPwd", None),
            new_pwd = self.get_argument("newPwd", None),
            new_pwd_repeat = self.get_argument("newPwdRepeat", None)
        )
        for k in args.keys():
            if( not args[k]):
                errors.append(u"complete the blanks")
                self.write(json.dumps(errors))
                self.finish()

        master = self.get_current_user()
        origin_pwd_hashed = hashlib.sha512(args['origin_pwd']).hexdigest()
        if master['pwd'] == origin_pwd_hashed:
            if args['new_pwd'] == args['new_pwd_repeat']:
                master['pwd'] = hashlib.sha512(args['new_pwd']).hexdigest()
                master['auth'] = hashlib.sha512(master['name'] + master['pwd']).hexdigest()
                da.save_member(master)
                # update secure cookie
                self.set_cookie(name="auth", 
                            value=master['auth'], 
                            expires_days = 365)
            else:
                errors.append(u"新密码两次输入不一致")
        else:
            errors.append(u"当前密码输入错误")
        if len(errors) > 0:
            self.write(json.dumps(errors))
        else:
            self.write(json.dumps(True))
        self.finish()

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", title="Login", errors=None, master=False)

    def post(self):
        template = "login.html"
        errors = []

        args = dict(
            name = self.get_argument("name", None),
            pwd = self.get_argument("pwd", None)
        )
        if( not args['name'] or not args['pwd']):
            errors.append(u"complete the blanks")
            self.render(template, 
                        title="Login", 
                        master=False, 
                        errors=errors)

        try:
            member = da.get_member_by_name(args['name'])
            input_auth = hashlib.sha512(args['name'] + 
                        hashlib.sha512(args['pwd']).hexdigest()).hexdigest()
        except:
            errors.append(u"db error")

        if member and (member['auth'] == input_auth):
            self.set_cookie(name = "auth", 
                            value = member['auth'], 
                            expires_days = 365)
        else:
            errors.append(u"error with user name or password") 
        if len(errors) > 0:
            self.render(template, 
                        title = "Login", 
                        master = False, 
                        errors = errors)
        else:
            self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')
     

class ForgetHandler(BaseHandler):
    def get(self):
        self.render("forget.html", 
            title="Login", 
            errors=None, 
            master=False)

    def post(self):
        errors = []
        template = "forget.html"

        args = dict(
            name = self.get_argument("name", None),
            email = self.get_argument("email", None)
        )
        if( not args['name'] or not args['email']):
            errors.append(u"complete the blanks")
            self.render(template, 
                        title="Forget", 
                        master=False, 
                        errors=errors)

        member = da.get_member_by_name(args['name'])
        if member:
            if args['email'] == member['email']:
                member['secret_key']  = randomwords(20)
                da.save_member(member)
                send_verification_email(args['email'], member['secret_key'])
            else:
                errors.append(u"email is wrong")
        else:
            errors.append(u"no such user")
        if len(errors) > 0:
            self.render("forget.html", 
                        title = "Forget", 
                        master = False, 
                        errors = errors)
        else:
            self.redirect("/")

class PasswordHandler(BaseHandler):
    def get(self):
        secret_key = self.get_argument("key", None)
        member = da.get_member_by({"secret_key": secret_key})
        if member:
            self.render("password.html", 
                title="Change Password", 
                errors=None, 
                master=False, 
                key=secret_key)
        else:
            self.send_error(404)
            self.finish()

    def post(self):
        #
        # Use secret_key to get the very user who send change password request
        # Replace old password with the new one.
        # update everything related to the password, like auth string, secure cookie , etc.
        #
        errors = []
        args = dict(
            pwd = self.get_argument("pwd", None),
            cpwd = self.get_argument("pwd", None)
        )
        if( not args['name'] or not args['pwd']):
            errors.append(u"complete the blanks")
            self.render(template, 
                        title="Login", 
                        master=False, 
                        errors=errors)
        pwd = self.get_argument("pwd", None)
        cpwd = self.get_argument("cpwd", None)
        secret_key = self.get_argument("key", None)

        member = da.get_member_by({"secret_key": secret_key})
        if member:
            if pwd == cpwd:
                member['pwd'] = hashlib.sha512(pwd).hexdigest()
                member['auth'] = hashlib.sha512(member['name'] + member['pwd']).hexdigest()
                del member['secret_key']
                da.save_member(member)
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

def randomwords(length):
    return ''.join(random.choice(string.lowercase 
                + string.uppercase + string.digits) for i in range(length))
