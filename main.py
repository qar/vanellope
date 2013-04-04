#! /usr/bin/env python
# coding=utf-8

import os
import sys
import os.path
import logging
import urls

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

from vanellope.handlers import BaseHandler

options['log_file_prefix'].set('log/page302.log')
define("port", default=8000, help="run on the given port", type=int)

ROOT = os.path.abspath(os.path.dirname(__file__))

class App(tornado.web.Application):
    def __init__(self):
        SETTINGS = dict(
            static_path = os.path.join(ROOT, 'static'),
            template_path = os.path.join(ROOT, 'templates'),
            login_url = "/login",
            debug = True
        )

        tornado.web.Application.__init__(self, urls.handlers, **SETTINGS)


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


