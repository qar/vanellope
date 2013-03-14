#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import datetime
from vanellope.handlers import BaseHandler
from vanellope.ext import db


import tornado.web

UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
EMAIL_ERR = {
    # the dict key MUST NOT be changed
    'exist': u"This email address has being used",
    'invalid': u"It's not a valid email address",
}

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

        self.render("memberHomePage.html",
                    title = author['name']+u"专栏",
                    articles = articles,
                    master = self.get_current_user(),
                    pages = pages,
                    author = author)


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
            model['pwd'] = args['pwd']
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
            model['auth'] = hashlib.sha512(model['email'] + model['pwd']).hexdigest()
            gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
                             hashlib.md5(email.lower()).hexdigest() + "?")
            gravatar_url += urllib.urlencode({'s':str(size)})
            model['avatar'] = gravatar_url
            db.member.insert(model)
            self.set_cookie(name="auth", 
                            value=model['auth'], 
                            expires_days = 365)
            self.redirect('/')
