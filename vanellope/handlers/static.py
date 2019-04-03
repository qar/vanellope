# coding=utf-8

import os
from tornado.web import StaticFileHandler

class MyStaticFileHandler(StaticFileHandler):
    def initialize(self, path, default_filename=None):
        super(StaticFileHandler, self).initialize()

        root_path = self.settings['root_path']
        theme = self.settings['theme']
        if path.startswith('/src/vanellope/themes'):
            self.root = os.path.join(root_path, 'themes/%s/static/' % theme)
        else:
            self.root = path
