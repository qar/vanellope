# coding=utf-8

import os
from tornado.web import StaticFileHandler

class MyStaticFileHandler(StaticFileHandler):
    def initialize(self, path, default_filename=None):
        super(StaticFileHandler, self).initialize()

        if self.settings.get('admin_static_path'):
            # Those are admin related file, have nothing to do with themes
            self.root = path
            return

        theme = self.settings['theme']

        buildin_themes_dir = self.settings['themes_dir']
        custom_themes_dir = self.settings['custom_themes_dir']

        buildin_themes = os.listdir(buildin_themes_dir)
        custom_themes = os.listdir(custom_themes_dir)

        theme_related = theme in buildin_themes or theme in custom_themes

        if not theme_related:
            self.root = path
            return

        if theme in buildin_themes:
            self.root = os.path.join(buildin_themes_dir, '%s/static/' % theme)
        else:
            self.root = os.path.join(custom_themes_dir, '%s/static/' % theme)
