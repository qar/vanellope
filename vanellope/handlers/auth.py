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
from vanellope import db
from vanellope import Mail
from vanellope import regex
from vanellope import exception

from vanellope.model import Member
from vanellope.handlers import BaseHandler


class RegisterHandler(BaseHandler):
    def get(self):
        current_user = self.get_current_user()
        self.render("register.html", 
                    title = '注册',
                    errors = None,
                    master = current_user)

    @tornado.web.asynchronous
    def post(self):
        errors = [] # errors message container
        member = Member()
        post_values = ['name','pwd','cpwd','email']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)

        # Set user name
        try:
            member.set_name(args['name'])
        except exception.NameError:
            errors.append(u"请填写用户名")
        except exception.DupKeyError:
            errors.append(u"用户名已经被使用")
        except exception.PatternMatchError:
            errors.append(u"你填写的用户名中有不被支持的字符")

        # Set user password
        if args['pwd'] != args['cpwd']:
            errors.append(u"两次输入的密码不一致")
        elif args['pwd'] is None and args['cpwd'] is None:
            errors.append(u"请填写密码")
        else:
            member.set_password(args['pwd'])

        # set user email
        try:
            member.set_email(args['email'])
        except ValueError:
            errors.append(u"请填写邮箱")
        except exception.DupKeyError:
            errors.append(u"邮箱已经被使用")
        except exception.PatternMatchError:
            errors.append(u"邮件地址格式不正确")

        if errors:
            self.render("register.html", 
                        title = u"注册", 
                        errors = errors,    
                        master = None)
        else:
            member.set_secret_key(randomwords(20))
            member.verify()
            member.put()
            self.set_cookie(name="auth", 
                            value=member.auth, 
                            expires_days = 365)
            self.redirect('/')


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", 
                    title="Login", 
                    errors=None, 
                    master=None)

    def post(self):
        errors = []
        template = "login.html"
        post_values = ['name','pwd']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)
        
        try:
            # BUG: can not chain like this "member = Member().reload()"
            member = Member()
            member.reload(args['name'], args['pwd'])
            self.clear_all_cookies()
            self.set_cookie(name = "auth", 
                            value = member.auth,
                            expires_days = 365)
            self.redirect("/")
        except exception.NameError:
            errors.append(u"请填写用户名")
        except exception.AuthError:
            errors.append(u"用户名或密码错误")
        
        if len(errors) > 0:
            # No need to go on either name or pwd is None
            self.render(template, 
                        title = "Login", 
                        master = None, 
                        errors = errors)


class LogoutHandler(BaseHandler):
    def get(self):
        referer = self.request.headers['Referer']
        self.clear_all_cookies()
        self.redirect(referer)


class VerifyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #
        # Database member entity's "verified" tag is initially "False"
        # until this method is called.
        #
        # TODO: complete notification message display
        #
        errors = []
        secret_key = self.get_argument("key", None)
        
        current_user = self.current_user_entity()
        if not current_user.verified:
            # Verify secret key and set "verified" tag to "True"
            if secret_key == current_user.secret_key:
                current_user.getverified()
                current_user.put()
                self.redirect("/") # everything fine
            else:
                self.send_error(403) # url insecure
        else:
            self.redirect("/") # email has been verified
        self.finish()


class ForgetHandler(BaseHandler):
    def get(self):
        self.render("forget.html", 
            title="Login", 
            errors=None, 
            master=None)

    def post(self):
        errors = []
        template = "forget.html"
        post_values = ['name','email']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)

        if args['name'] is None:
            errors.append(u"请填写用户名")
        elif args['email'] is None:
            errors.append(u"请填写邮箱")
        else:
            member = da.get_member_by_name(args['name'])
            if not member:
                errors.append(u"这个用户不存在")
            elif args['email'].lower() != member['email']:
                errors.append(u"不是用户注册时使用的邮箱")
            elif not member.verified:
                errors.append(u"此邮箱未通过验证，不能用于找回密码")
            else:
                member.set_secret_key(randomwords(20))
                member.put()
                self.send_email(member['email'], member.secret_key)

        if len(errors) > 0:
            self.render("forget.html", 
                        title = "找回密码", 
                        master = None, 
                        errors = errors)
        else:
            self.redirect("/")

    def send_email(self, email, key):
        netloc = urlparse.urlsplit(config.HOSTNAME).netloc
        URL = "%s/password?" % (config.HOSTNAME,)+urllib.urlencode({"key":key})
        SUBJECT = "[%s]找回密码" % netloc
        CONTENT = '''
        <p>点击下面的链接或将其复制到浏览器地址栏中打开来设密重码</p>
        <a href="%s">%s</a>
        ''' % (URL, URL)
        mail = Mail(Subject=SUBJECT, To=email, Body=CONTENT)
        mail.Send()


class PasswordResetHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):        
        #
        # This method is called when LOGINED user intend to change password.
        # Origin password is required to prevent malicious option.
        #
        msg = []
        post_values = ['originPwd','newPwd','newPwdRepeat']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)


        master = self.current_user_entity()
        if master.check_password(args['originPwd']):
            if args['newPwd'] == args['newPwdRepeat']:
                try:
                    master.set_password(args['newPwd'])
                    master.put()
                    self.clear_all_cookies()
                    self.set_cookie("auth", master.auth)
                except TypeError:
                    msg.append(u"密码不能为空")
            else:
                msg.append(u"新密码两次输入不一致")
        else:
            msg.append(u"当前密码输入错误")
        self.finish(json.dumps(msg))



class PasswordHandler(BaseHandler):
    def get(self):
        secret_key = self.get_argument("key", None)
        member = db.member.find_one({"secret_key": secret_key})
        if member:
            self.render("password.html", 
                        title="更改密码", 
                        errors=None, 
                        master=None, 
                        key=secret_key)
        else:
            self.send_error(404)
            self.finish()

    def post(self):
        #
        # Use secret_key to get the user who send change password request.
        # Replace old password with the new one.
        # update everything related to the password, 
        # like auth string, secure cookie , etc.
        #
        errors = []
        post_values = ['pwd','cpwd', 'key']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)
    
        member = db.member.find_one({"secret_key": args['key']})
        master = self.current_user_entity()
        if args['pwd'] == args['cpwd']:
            try:
                master.set_password(args['pwd'])
                master.put()
                self.clear_all_cookies()
                self.set_cookie("auth", master.auth)
            except TypeError: # this try/except has no "else" statement
                errors.append(u"密码不能为空")
        else:
            errors.append(u"新密码两次输入不一致")
        if len(errors) > 0:
            self.render("password.html", 
                        title="更改密码", 
                        errors=errors, 
                        master=False, 
                        key=args['key'])
        else:
            self.redirect("/home")


def randomwords(length):
    random.seed()
    return ''.join(random.choice(string.lowercase 
                + string.uppercase + string.digits) for i in range(length))
