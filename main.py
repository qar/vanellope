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

from vanellope.model import Article
from vanellope.model import Comment
from vanellope.handlers.member import MemberHandler
from vanellope.handlers.member import RegisterHandler
from vanellope.handlers.article import ArticleHandler
from vanellope.handlers.article import ArticleUpdateHandler

from vanellope.handlers import BaseHandler
from vanellope.ext import db

import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.httpserver

sys.path.append(os.getcwd())
from tornado.options import define, options

options['log_file_prefix'].set(os.path.join(os.path.dirname(__file__), 'page302.log'))
define("port", default=8000, help="run on the given port", type=int)





class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/register", RegisterHandler),
        (r"/article/([0-9]+)", ArticleHandler),
        (r"/article", ArticleHandler),
        (r"/home", HomeHandler),
        (r"/u/(.*)", MemberHandler),
        (r"/home/(.*)", HomeHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/update/(.*)", ArticleUpdateHandler),
        (r"/comment/(.*)", CommentHandler)]

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

        #top_x_hotest = db.article.find({"status":"normal"})
        #top_x_hotest.sort("heat", -1).limit(10)

        total = db.article.count()
        pages  = total // 10 + 1
        if total % 10 > 0:
            pages += 1

        self.render("index.html", 
                    title = 'PAGE302',
                    master = self.get_current_user(), 
                    pages = pages,
                    articles = articles)






class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", title="Login", errors=None, master=False)

    def post(self):
        template = "login.html"
        errors = []
        
        post_values = ['name','pwd']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                errors.append("complete the blanks")
                self.render(template, 
                            title="Login", 
                            master=False, 
                            errors=errors)
        try:
            member = db.member.find_one({'name':args['name']})
            input_auth = hashlib.sha512(args['name'] + 
                        hashlib.sha512(args['pwd']).hexdigest()).hexdigest()
        except:
            errors.append("db error")
            self.render(template, 
                        title = "Login",
                        master = False, 
                        errors = errors)

        if member and (member['auth'] == input_auth):
            self.set_cookie(name = "auth", 
                            value = member['auth'], 
                            expires_days = 365)
            self.redirect('/')
        else:
            errors.append("error with user name or password") 
            self.render(template, 
                        title = "Login", 
                        master = False, 
                        errors = errors)
  


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page="index"):
        pages = ('write', 'manage', 'setting', 'index')
        template = ("home/%s.html" % page)
        master = self.get_current_user()
        if (page == "manage"):
            articles = self.normal_articles(master['uid'])
            self.render(template, 
                        title = 'HOME | manage', 
                        master = master,
                        articles = articles)
        else:
            self.render(template, 
                        title="Home",
                        master = master)

    @tornado.web.authenticated
    def post(self):
        master = self.get_current_user()
        if master:
            brief = self.get_argument('brief', default=None)
            db.member.update({"uid":master['uid']},{"$set":{"brief":brief}})
            member = db.member.find_one({'uid': master['uid']})
        else:
            self.send_error(403)
            self.findish()

    def get_author_all_articles(self, owner_id):
        return db.article.find({"author": owner_id}).sort("date", -1)

    def normal_articles(self, owner_id):
        return db.article.find(
                {"author": owner_id, "status":"normal"}).sort("date", -1)
        





class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, article_sn):
        master = self.get_current_user()
        # if comment has no content then return back silently.
        try:
            cmt = self.get_argument('comment')
        except:
            self.redirect(self.request.headers['Referer'])

        comment = Comment(int(article_sn))

        if master:
            # basic commenter information
            commenter = {
                "uid": master['uid'],
                "name": master['name'],
                "name_safe": master['name_safe'],
                "avatar": master['avatar']
            }
            comment.set_commenter(commenter)
            comment.set_content(cmt)
            comment.save()
            self.redirect("/article/%s" % article_sn)
        else:
            self.send_error(403)




if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


