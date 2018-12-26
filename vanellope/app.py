#! /usr/bin/env python
# coding=utf-8

import re
import os
import os.path
import sys
sys.path.append(os.getcwd())

from tornado import web
from tornado import ioloop
from tornado.options import define, options
from vanellope.da import init_db, connection
from vanellope.da.user import UserModel
from vanellope import config
from vanellope.urls import routers

define("port", default=8000, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="run on the given host", type=str)
define("debug", default=False, help="debug mode.", type=bool)

ROOT = os.path.abspath(os.path.dirname(__file__))


def get_admin_user():
    return UserModel().get_admin_user()


def preflight():
    # check content path existence
    pass


class App(web.Application):
    def __init__(self):

        init_db()

        theme = config.theme
        static_path = os.path.join(ROOT, "themes/%s/static" % theme)
        template_path = os.path.join(ROOT, "themes/%s/templates" % theme)
        admin_static_path = os.path.join(ROOT, "admin/assets")
        admin_template_path = os.path.join(ROOT, "admin/templates")
        config_keys = config.app_settings.keys()

        settings = {
            "static_path": static_path,
            "template_path": template_path,
            "admin_static_path": admin_static_path,
            "admin_template_path": admin_template_path,
            "static_url_prefix": "/static/",
            "admin_static_url_prefix": "/assets/",
            "config_keys": config_keys,
            "uploaded_path": config.uploaded_path,
            "db_path": config.db_path,

            # None or dict object
            # Indicating whether or not the site has a registered admin user
            "admin": get_admin_user(),
            "theme": theme,

            "include_version": True,
            "login_url": "/login",
            "debug": options.debug,
            "db_conn": connection
        }

        if settings.get("admin_static_path"):
            path = settings["admin_static_path"]
            static_url_prefix = settings.get("admin_static_url_prefix",
                                             "/static/")
            static_handler_class = settings.get("static_handler_class",
                                                web.StaticFileHandler)
            static_handler_args = settings.get("admin_static_handler_args", {})
            static_handler_args["path"] = path
            for pattern in [re.escape(static_url_prefix) + r"(.*)",
                            r"/(favicon\.ico)", r"/(robots\.txt)"]:
                routers.insert(0, (pattern, static_handler_class,
                                   static_handler_args))

        web.Application.__init__(self, routers, **settings)

    def log_request(self, handler):
        pass


def make_app():
    return App()


def main():
    options.parse_command_line()
    App().listen(options.port, options.host, xheaders=True)
    print "VANELLOPE running on %s:%d" % (options.host, options.port)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    preflight()
    main()
