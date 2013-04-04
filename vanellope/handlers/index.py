#! /usr/bin/env python
# coding=utf-8


from vanellope import da
from vanellope.handlers import BaseHandler

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


handlers = [
	(r"/", IndexHandler),
]