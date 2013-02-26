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
from page302.utility import *
from page302.security import CheckAuth

from tornado.options import define, options


options['log_file_prefix'].set(settings.LOG_LOCATION)
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/register", RegisterHandler),
        (r"/article/([0-9]+.*)", ArticleHandler),
        (r"/article", ArticleHandler),
        (r"/home", HomeHandler),
        (r"/u/(.*)", MemberHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/test", TestHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/comment/(.*)", CommentHandler)]
        
        self.db = settings.DATABASE

        SETTINGS = dict(
        static_path = settings.STATIC_PATH,
        template_path = settings.TEMPLATE_PATH,
        debug = settings.DEBUG)

        tornado.web.Application.__init__(self, handlers, **SETTINGS)

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello, world")

class MemberHandler(tornado.web.RequestHandler):
    def get(self, uname):
        db_member = self.application.db.member
        db_article =  self.application.db.article
        master = CheckAuth(self.get_cookie('auth'))

        template = "memberHomePage.html"
        author = db_member.find_one({"name_low": uname})
        articles = db_article.find({"author_id": author['_id']}).sort("date",-1)
        self.render(template,
                    title = "PAGE302",
                    articles = articles,
                    master = master,
                    author = author)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        db_member = self.application.db.member
        db_article = self.application.db.article
        template = 'index.html'

        master = CheckAuth(self.get_cookie('auth'))
        articles = db_article.find().sort("date",-1)
        top_x_hotest = db_article.find({}).sort("heat", -1).limit(10)

        self.render(template, 
                    title = 'PAGE302',
                    master = master, 
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
            member = db_member.find_one({'name_low':args['name'].lower()})
            input_auth = hashlib.sha512(args['name'].lower() + 
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
            articles = self.get_author_all_articles(master['_id'])
            self.render(template, 
                        title = 'HOME | manage', 
                        master = master,
                        articles = articles)
        else:
            self.render(template, 
                        title="Home",
                        master = master)

    def get_author_all_articles(self, member_id):
        articles = self.application.db.article.find(
                    {"author_id": member_id}).sort("date", -1)
        return articles



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


