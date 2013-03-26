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

from vanellope import db
from vanellope import Mail

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

CSS_COlOR_PATT = r"#[0-9a-fA-F]{6}"


class ColorHandler(BaseHandler):
    def post(self):
        color = self.get_argument("color", None)
        if re.match(CSS_COlOR_PATT, color):
            master = self.get_current_user()
            master['color'] = color
            db.member.save(master)
            return True
        else:
            return False



