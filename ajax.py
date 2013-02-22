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
from page302.utility import *
from page302.security import CheckAuth

class AjaxHandler(tornado.web.RequestHandler):
	def get(self):
		pass

	def post(self, cotent):
		self.write('hello,'+content)

