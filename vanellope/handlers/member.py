#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import datetime
import smtplib
import string
import random
import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from vanellope.ext import db
from vanellope.handlers import BaseHandler

import tornado.web
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



UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
EMAIL_ERR = {
    # the dict key MUST NOT be changed
    'exist': u"This email address has being used",
    'invalid': u"It's not a valid email address",
}
CSS_COlOR_PATT = r"#[0-9a-fA-F]{6}"

class MemberHandler(BaseHandler):
    def get(self, uname):
        page = self.get_argument("p", 1)
        skip_articles = (int(page) -1 )*10
        author = db.member.find_one({"name_safe": uname})
        articles = db.article.find({"status":"normal",
                                    "author": author['uid']}).sort("date",-1).limit(skip_articles)

        total = db.article.find({"author": author['uid']}).count()
        pages  = total // 10 + 1
        if total % 10 > 0:
            pages += 1

        self.render("index.html",
                    title = author['name']+u"专栏",
                    articles = articles,
                    master = self.get_current_user(),
                    pages = pages,
                    author = author)

    @tornado.web.authenticated
    def post(self):
        try:
            color = self.get_argument("color")
            if re.match(CSS_COlOR_PATT, color):
                master = self.get_current_user()
                master['color'] = color
                db.member.save(master)
                return True
            else:
                return False
        except:
            return False
    


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
        try:
            for v in post_values:
                args[v] = self.get_argument(v, None)
        except:
            errors.append("complete the blanks")
            html = render_string("register.html", title = "Reqister", 
                        master = None, errors = errors)
            self.write(html)

        # set user name
        # check user input name's usability
        if re.match(UID_PATT, args['name']):
            if db.member.find_one({"name": args['name']}):
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
            if db.member.find_one({"email": args['email'].lower()}):
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
            model['uid'] = db.member.count() + 1
            model['date'] = datetime.datetime.utcnow()
            model['auth'] = hashlib.sha512(model['name'] + model['pwd']).hexdigest()
            gravatar = ("http://www.gravatar.com/avatar/%s" % 
                             hashlib.md5(model['email']).hexdigest() + "?")
            model['avatar'] = gravatar + urllib.urlencode({'s':64})
            model['avatar_large'] = gravatar + urllib.urlencode({'s':128})
            model['secret_key'] = randomwords(20)
            send_verification_email(model['email'], model['secret_key'])
            db.member.insert(model)

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
                db.member.save(master)
                self.write("your email is activated\n") # everything fine
            else:
                self.write("url invalid") # url insecure
        else:
            self.write("your email has been activated already") # email has been verified
        self.finish()


class ResetHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        errors = []
        origin_pwd = self.get_argument("origin_pwd", None)
        new_pwd = self.get_argument("new_pwd", None)
        new_pwd_repeat = self.get_argument("new_pwd_repeat", None)

        master = self.get_current_user()
        origin_pwd_hashed = hashlib.sha512(origin_pwd).hexdigest()

        if master['pwd'] == origin_pwd_hashed:
            if new_pwd == new_pwd_repeat:
                new_pwd_hashed = hashlib.sha512(new_pwd).hexdigest()
                master['pwd'] = new_pwd_hashed
                master['auth'] = hashlib.sha512(master['name'] + new_pwd_hashed).hexdigest()
                db.member.save(master)

                self.set_cookie(name="auth", 
                            value=master['auth'], 
                            expires_days = 365)
                self.set_status(200)
                self.render("home/index.html", 
                        title="Home",
                        errors = errors,
                        master = master)
            else:
                errors.append(u"新密码两次输入不一致")
                self.render("home/index.html", 
                        title="Home",
                        errors = errors,
                        master = master)

        else:
            errors.append(u"当前密码输入错误")
            self.render("home/index.html", 
                        title="Home",
                        errors = errors,
                        master = master)



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

        name = self.get_argument("name", None)
        email = self.get_argument("email", None)

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
        secure_key = self.get_argument("key", None)
        member = db.member.find_one({"secure_key": secure_key})
        if member:
            self.render("password.html", title="Change Password", errors=None, master=False, key=secure_key)
        else:
            self.send_error(404)
            self.finish()

    def post(self):
        errors = []
        pwd = self.get_argument("pwd", None)
        cpwd = self.get_argument("cpwd", None)
        secure_key = self.get_argument("key", None)

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



def randomwords(length):
        return ''.join(random.choice(string.lowercase 
                + string.uppercase + string.digits     ) for i in range(length))

def send_verification_email(dst_email, secret_key):
    TO = dst_email
    url = "%s/verify/?" % (config.HOSTNAME,) + urllib.urlencode(
        {"secret_key":secret_key})
    CONTENT = '''
    <h1>Welcome ! </h1>
    <p>感谢您在 %s 注册, 复制下面的链接到浏览器地址栏进行验证</p>
    <p>%s</p>
    ''' % (config.HOSTNAME, url, )
    msg = MIMEText(CONTENT, 'html')
    msg['Subject'] = "Email Verification"
    msg['From'] = config.FROM_EMAIL
    msg['To'] = TO
    s = smtplib.SMTP(config.SMTP_SERVER)
    s.login(config.SMTP_SERVER_LOGIN[0], config.SMTP_SERVER_LOGIN[1])
    s.sendmail(config.FROM_EMAIL, [TO,], msg.as_string())
    s.quit()