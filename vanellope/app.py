#! /usr/bin/env python
# coding=utf-8

import re
import os
import os.path

from tornado import web
from tornado import ioloop
from tornado.options import define, options
from vanellope import config
from vanellope.database import create_tables, get_admin_user, connection
from vanellope.urls import routers

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="debug mode.", type=bool)

ROOT = os.path.abspath(os.path.dirname(__file__))


class App(web.Application):
    def __init__(self):

        create_tables()

        theme = config.theme
        static_path = os.path.join(ROOT, 'themes/%s/static' % theme)
        template_path = os.path.join(ROOT, 'themes/%s/templates' % theme)
        admin_static_path = os.path.join(ROOT, 'admin/static')
        admin_template_path = os.path.join(ROOT, 'admin/templates')
        config_keys = config.app_settings.keys()

        settings = {
            "static_path": static_path,
            "template_path": template_path,
            "admin_static_path": admin_static_path,
            "admin_template_path": admin_template_path,
            "static_url_prefix": "/static/",
            "admin_static_url_prefix": "/admin-static/",
            "config_keys": config_keys,
            "uploaded_path": config.uploaded_path,
            "db_path": config.db_path,

            # None or dict object
            # Indicating whether or not the site has a registered admin user
            "admin": get_admin_user(),
            "theme": theme,

            "include_version": True,
            "login_url": '/login',
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
            static_handler_args['path'] = path
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
    App().listen(options.port, '127.0.0.1', xheaders=True)
    print 'VANELLOPE running on %d' % options.port
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
