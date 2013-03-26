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
from vanellope.ext import Mail

from vanellope.model import Article
from vanellope.model import Comment

from vanellope.handlers import BaseHandler
from vanellope.handlers import ajax

from vanellope.handlers.auth import LoginHandler
from vanellope.handlers.auth import LogoutHandler
from vanellope.handlers.auth import ForgetHandler
from vanellope.handlers.auth import PasswordHandler
from vanellope.handlers.auth import VerifyHandler
from vanellope.handlers.auth import PasswordResetHandler
from vanellope.handlers.auth import RegisterHandler

from vanellope.handlers.member import MemberHandler
from vanellope.handlers.member import EmailHandler
from vanellope.handlers.member import HomeHandler

from vanellope.handlers.comment import CommentHandler

from vanellope.handlers.article import ArticleHandler
from vanellope.handlers.article import PagesHandler
from vanellope.handlers.article import HotestHandler
from vanellope.handlers.article import RecoverHandler
from vanellope.handlers.article import ArticleUpdateHandler

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver
from tornado.options import define, options

UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
sys.path.append(os.getcwd())

options['log_file_prefix'].set(os.path.join(os.path.dirname(__file__), 'page302.log'))
define("port", default=8000, help="run on the given port", type=int)


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", IndexHandler),

        (r"/home", HomeHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/member", MemberHandler),
        (r"/member/([a-zA-Z0-9]{1,16})", MemberHandler),
        (r"/member/email\.json", EmailHandler),
        
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/reset", PasswordResetHandler),
        (r"/password", PasswordHandler),
        (r"/register", RegisterHandler),
        (r"/forget", ForgetHandler),
        (r"/verify/", VerifyHandler),

        (r"/article", ArticleHandler),
        (r"/article/([0-9]+)", ArticleHandler),
        (r"/article/page/([0-9]+)\.json", PagesHandler),
        (r"/article/recover/([0-9]+)", RecoverHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/article/hotest/([0-9]+)", HotestHandler),

        (r"/comment/(.*)", CommentHandler),
        (r"/widgets/([-\w\d]*\.html$)", WidgetsHandler),
        (r"/ajax/color", ajax.ColorHandler),]

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
        total = db.article.find({"status":"normal"}).count()
        pages = total // 10 + 1 # pages count from 1
        if total % 10 > 0:      # the last page articles may not equal to 'p' 
            pages += 1 

        self.render("index.html", 
                    title = 'PAGE302',
                    master = self.get_current_user(), 
                    pages = pages,
                    articles = articles)


class WidgetsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, w=None):
        path = os.path.join(self.application.settings['template_path'],'widgets',w)
        print path
        if os.path.exists(path):
            f = open(path, 'r')
            self.finish(f.read())
        else:
            self.send_error(404)
            self.finish()



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


