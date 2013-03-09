#! /usr/bin/env python
# coding=utf-8

import os
import sys
import os.path
import hashlib
import datetime
import time
import logging
import re
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

import markdown
import settings

from handlers import *
from article import Article
from member import Member, CheckAuth, Avatar

from tornado.options import define, options


options['log_file_prefix'].set(settings.LOG_LOCATION)
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        self.db = settings.DATABASE
        handlers = [
        (r"/", IndexHandler),
        (r"/register", RegisterHandler),
        (r"/article/([0-9]+)", ArticleHandler),
        (r"/article", ArticleHandler),
        (r"/home", HomeHandler),
        (r"/u/(.*)", MemberHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/login", LoginHandler),
        (r"/test/?([^/]*)", TestHandler),
        (r"/logout", LogoutHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/comment/(.*)", CommentHandler)]

        SETTINGS = dict(
        static_path = settings.STATIC_PATH,
        template_path = settings.TEMPLATE_PATH,
        debug = settings.DEBUG)

        tornado.web.Application.__init__(self, handlers, **SETTINGS)

class TestHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.write("this is test page" + slug)       

class MemberHandler(tornado.web.RequestHandler):
    def get(self, uname):
        db_member = self.application.db.member
        db_article = self.application.db.article

        master = CheckAuth(self.get_cookie('auth'))
        #master = member.check_auth(self.get_cookie('auth'))

        template = "memberHomePage.html"
        author = db_member.find_one({"name_safe": uname})
        articles = db_article.find({"status":"normal",
                                    "author": author['uid']}).sort("date",-1)
        self.render(template,
                    title = author['name']+u"专栏",
                    articles = articles,
                    master = master,
                    author = author)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        db_member = self.application.db.member
        db_article = self.application.db.article
        template = 'index.html'

        page = self.get_argument("p", 1)
        skip_articles = (int(page) -1 )*10
        master = CheckAuth(self.get_cookie('auth'))
        #master = member.check_auth(self.get_cookie('auth'))
        articles = db_article.find({"status":"normal"}).sort("date",-1).skip(skip_articles).limit(10)
        top_x_hotest = db_article.find({"status":"normal"}).sort("heat", -1).limit(10)

        total = db_article.count()
        pages  = total // 10 + 1
        if total % 10 > 0:
            pages += 1

        self.render(template, 
                    title = 'PAGE302',
                    master = master, 
                    pages = pages,
                    articles = articles,
                    hotest = top_x_hotest)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        template = "login.html"
        self.render(template, title="Login", errors=None, master=False)

    def post(self):
        db_member = self.application.db.member
        template = "login.html"
        errors = []
        
        post_values = ['name','pwd']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                errors.append("complete the blanks")
                self.render(template, 
                            title="Login", 
                            master=False, 
                            errors=errors)
        try:
            member = db_member.find_one({'name':args['name']})
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
  


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


class HomeHandler(tornado.web.RequestHandler):
    def get(self, page="index"):
        db_member = self.application.db.member
        db_article = self.application.db.article
        pages = ('write', 'manage', 'setting', 'index')
        template = ("home/%s.html" % page)
        master = CheckAuth(self.get_cookie('auth'))
        if not master:
            self.send_error(401)
            self.finish()
        if (page == "manage"):
            articles = self.normal_articles(master['uid'])
            self.render(template, 
                        title = 'HOME | manage', 
                        master = master,
                        articles = articles)
        else:
            self.render(template, 
                        title="Home",
                        master = master)
    def post(self):
        db_member = self.application.db.member
        master = CheckAuth(self.get_cookie('auth'))
        if master:
            brief = self.get_argument('brief', default=None)
            db_member.update({"uid":master['uid']},{"$set":{"brief":brief}})
            member = db_member.find_one({'uid': master['uid']})
        else:
            self.send_error(403)
            self.findish()

    def get_author_all_articles(self, owner_id):
        db_article = self.application.db.article
        return db_article.find({"author": owner_id}).sort("date", -1)

    def normal_articles(self, owner_id):
        db_article = self.application.db.article
        return db_article.find(
                {"author": owner_id, "status":"normal"}).sort("date", -1)
        


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


