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
import markdown

from vanellope.ext import db
from vanellope.model import Article
from vanellope.model import Comment
from vanellope.handlers import BaseHandler
from vanellope.handlers.auth import LoginHandler
from vanellope.handlers.auth import LogoutHandler
from vanellope.handlers.auth import ForgetHandler
from vanellope.handlers.auth import PasswordHandler
from vanellope.handlers.comment import CommentHandler
from vanellope.handlers.member import MemberHandler
from vanellope.handlers.member import RegisterHandler
from vanellope.handlers.article import ArticleHandler
from vanellope.handlers.article import ArticleUpdateHandler

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver
from tornado.options import define, options

sys.path.append(os.getcwd())

options['log_file_prefix'].set(os.path.join(os.path.dirname(__file__), 'page302.log'))
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/register", RegisterHandler),
        (r"/article/([0-9]+)", ArticleHandler),
        (r"/article", ArticleHandler),
        (r"/home", HomeHandler),
        (r"/u/(.*)", MemberHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/login", LoginHandler),
        (r"/forget", ForgetHandler),
        (r"/member", MemberHandler),
        (r"/logout", LogoutHandler),
        (r"/password", PasswordHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/comment/(.*)", CommentHandler)]

        SETTINGS = dict(
        static_path = os.path.join(os.path.dirname(__file__), 'static'),
        template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        login_url = "/login",
        debug = True)

        tornado.web.Application.__init__(self, handlers, **SETTINGS)


      
class IndexHandler(BaseHandler):
    def get(self):
        page = self.get_argument("p", 1)
        skip_articles = (int(page) -1 )*10
        articles = db.article.find({"status":"normal"})
        articles.sort("date",-1).skip(skip_articles).limit(10)

        total = db.article.count()
        pages  = total // 10 + 1
        if total % 10 > 0:
            pages += 1

        self.render("index.html", 
                    title = 'PAGE302',
                    master = self.get_current_user(), 
                    pages = pages,
                    articles = articles)


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page="index"):
        pages = ('write', 'manage', 'setting', 'index')
        template = ("home/%s.html" % page)
        master = self.get_current_user()
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

    @tornado.web.authenticated
    def post(self):
        master = self.get_current_user()
        if master:
            brief = self.get_argument('brief', default=None)
            db.member.update({"uid":master['uid']},{"$set":{"brief":brief}})
            member = db.member.find_one({'uid': master['uid']})
        else:
            self.send_error(403)
            self.findish()

    def get_author_all_articles(self, owner_id):
        return db.article.find({"author": owner_id}).sort("date", -1)

    def normal_articles(self, owner_id):
        return db.article.find(
                {"author": owner_id, "status":"normal"}).sort("date", -1)
        


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


