#! /usr/bin/env python
# coding=utf-8

import os
import sys
import re
import os.path
import hashlib
import datetime
import time
import logging
import pymongo
import json
import markdown

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver
from tornado.options import define, options

from vanellope import da
from vanellope import db
from vanellope import Mail
from vanellope import regex
from vanellope import exception
from vanellope import constant as cst

from vanellope.model import Member
from vanellope.model import Article
from vanellope.model import Comment

from vanellope.handlers import BaseHandler

from vanellope.handlers.auth import LoginHandler
from vanellope.handlers.auth import LogoutHandler
from vanellope.handlers.auth import ForgetHandler
from vanellope.handlers.auth import PasswordHandler
from vanellope.handlers.auth import VerifyHandler
from vanellope.handlers.auth import PasswordResetHandler
from vanellope.handlers.auth import RegisterHandler

from vanellope.handlers.ajax import WidgetsHandler
from vanellope.handlers.ajax import ColorHandler
from vanellope.handlers.ajax import LikeHandler
from vanellope.handlers.ajax import ExportHandler
from vanellope.handlers.ajax import ContacterHandler

from vanellope.handlers.member import MemberHandler
from vanellope.handlers.member import EmailHandler
from vanellope.handlers.member import HomeHandler
from vanellope.handlers.member import BriefHandler
from vanellope.handlers.member import MessageHandler

from vanellope.handlers.comment import CommentHandler

from vanellope.handlers.article import ArticleHandler
from vanellope.handlers.article import PagesHandler
from vanellope.handlers.article import HotestHandler
from vanellope.handlers.article import RecoverHandler
from vanellope.handlers.article import ArticleUpdateHandler



options['log_file_prefix'].set('log/page302.log')
define("port", default=8000, help="run on the given port", type=int)


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", IndexHandler),

        (r"/ajax/like", LikeHandler),
        (r"/ajax/export/([0-9]+).json", ExportHandler),
        (r"/ajax/contacter", ContacterHandler),

        (r"/home", HomeHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/message", MessageHandler),
        (r"/brief", BriefHandler),
        (r"/member", MemberHandler),
        (r"/member/([0-9]{1,16})", MemberHandler),
        (r"/member/email\.json", EmailHandler),

        
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/reset", PasswordResetHandler),
        (r"/password", PasswordHandler),
        (r"/register", RegisterHandler),
        (r"/forget", ForgetHandler),
        (r"/verify", VerifyHandler),

        (r"/article", ArticleHandler),
        (r"/article/([0-9]+)", ArticleHandler),
        (r"/article/page/([0-9]+)\.json", PagesHandler),
        (r"/article/recover/([0-9]+)", RecoverHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/article/hotest/([0-9]+)", HotestHandler),
        
        (r"/comment/(.*)", CommentHandler),
        (r"/widgets/([-\w\d]*\.html$)", WidgetsHandler),
        (r"/ajax/color", ColorHandler),]

        SETTINGS = dict(
        static_path = os.path.join(os.path.dirname(__file__), 'static'),
        template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        login_url = "/login",
        debug = True)

        tornado.web.Application.__init__(self, handlers, **SETTINGS)


      
class IndexHandler(BaseHandler):
    def get(self):
        page = self.get_argument("p", 1)
        d = da.split_pages(page=page)
        current_user = self.get_current_user()
        self.render("index.html", 
                    title = 'PAGE302',
                    master = current_user, 
                    pages = d['pages'],
                    articles = d['articles'])


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


