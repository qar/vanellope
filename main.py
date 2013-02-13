#! /usr/bin/env python
# coding=utf-8

import os.path
import hashlib
import datetime
import time
import re
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

import markdown
from page302.utility import *
from page302.security import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", IndexHandler),
                (r"/register", RegisterHandler),
                (r"/archive/([0-9]+.*)", ArticleHandler),
                (r"/article", ArticleHandler),
                (r"/home", HomeHandler),
                (r"/home/(.*)", HomeHandler),
                (r"/u/(.*)", UserHandler),
                (r"/login", LoginHandler),
                (r"/logout", LogoutHandler),
                (r"/epictest", TestHandler),
                (r"/test", TestHandler),
                (r"/ajax", AjaxHandler),]
        
        settings = dict(
                static_path = os.path.join(
                        os.path.dirname(__file__), "static"),
                template_path = os.path.join(
                        os.path.dirname(__file__), "template"),
                debug = True)

        conn = pymongo.Connection('localhost',27017)
        self.db = conn['page302']
        tornado.web.Application.__init__(self, handlers, **settings)


class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        target = self.get_argument("t")
        if target == "demo":
            self.write("hello, world")


    def post(self):
        db_article = self.application.db.article
        #
        #target = self.get_argument("t")
        #if target == 'test':
        #    self.write("received")      
        #elif target == 'save':
        #    self.write("content received.")
        target = self.get_argument("o")
        if target == "del":
            db_article.remove({"sn": self.get_argument("sn")})
            



class TestHandler(tornado.web.RequestHandler):
    # XXX
    # delet this and related content when project finished.
    def get(self):
        template = "test.html"
        some_json = {
        "name": "Anran",
        "age": 23,
        "sex": "male",
        }
        content_test = "<h1>this is test content</h1>"
        #self.write(some_json)
        self.render(template, content_test = content_test)

class ArticleHandler(tornado.web.RequestHandler):
    def get(self, article_sn):
        db_member = self.application.db.member
        db_article = self.application.db.article

        template = "article.html"

        tpl_values = {
            'auth': False,
            'isauthor': False,     # indicate whether the current viewer
                                    # is the author
            'title': "", # article title
            'author_name': "", # author name
            'author_name_l': "", # author name lowercase 
            'name': "",  # member name
            'name_l': "", # member name lowercase
        }      

        try:
            # check whether viewer is a signed member
            member = CheckAuth(self.get_cookie('auth'))

            # get aritcle info from database and increase 'heat' value by one
            article = db_article.find_one({'sn': article_sn})
            article['heat'] += 1
            db_article.save(article)
            md = markdown.Markdown(safe_mode = "escape")

            article['content'] = md.convert(article['content'])
            #article['content'] = tornado.escape.xhtml_unescape(article['content'])
            
            # get author information from database
            author = db_member.find_one(
                        {'name_low': article['author']})

            tpl_values['author_name'] = author['name']
            tpl_values['author_name_l'] = author['name_low']
            tpl_values['title'] = article['title']

            try:
                tpl_values['author_brief'] = author['brief']
            except:
                tpl_values['author_brief'] = ""

            if member:
                tpl_values['auth'] = True
                tpl_values['name'] = member['name']
                tpl_values['name_l'] = member['name_low']
                if member['auth'] == author['auth']:
                    tpl_values['isauthor'] = True

            # pass mongodb cursor to template
            self.render(template, 
                    tpl_values = tpl_values, 
                    article = article)
        except:
           self.send_error(500)
        

    def post(self):
        db_article = self.application.db.article
        db_member = self.application.db.member

        article = {
            'sn':  None,   # seril number
            'date': None,
            'title': time.time(),
            'subtitle': '',
            'content': '',
            'author': '',
            'heat': 0,
            'link': {}, # name are captions of the related link
            'img': [], #imgs[0] should be intro-image
        }
        post_values = ['title','subtitle',
                       'intro-img','content','link']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass
        article['sn'] = str(db_article.count())
        article['title'] = args['title']
        article['subtitle'] = args['subtitle']
        article['content']  =args['content']
        
        # deal with uploaded file
        # BUG: only works when the current working directory is when the main.py file located
        upload_file = self.request.files['intro-img'][0]
        fpath = 'static/img/article/%s-intro.%s' %  (article['sn'], upload_file['filename'].split('.')[-1])
        fp = os.path.join(os.path.dirname(__file__), fpath)
        pic =  open(fp, 'wb')
        pic.write(upload_file['body'])
        pic.close()
        article['img'] = fpath

        try:     
            cookie_auth = self.get_cookie("auth")
            member = CheckAuth(self.get_cookie('auth'))
            if member:
                article['author'] =   member['name_low']  
                db_article.save(article)
                self.redirect('/')
            else:
                send_error(401)
        except:
            self.send_error(500)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        template = 'index.html'
        db_member = self.application.db.member
        db_article = self.application.db.article
        
        tpl_values = {
            'auth': False,
            'title': "INDEX",
            'name': "",
            'name_l': "",}

        newest = []
        cookie_auth = self.get_cookie("auth")
        articles = db_article.find().sort("date",-1)
        for a in articles:
            newest.append((a['sn'],a['title']))
        articles = db_article.find().sort("date",-1)
        #articles    = db_article.find().sort("sn",-1).limit(3)
        member = CheckAuth(self.get_cookie('auth'))
        if member:
            tpl_values['auth'] = True
            tpl_values['name'] = member['name']
            tpl_values['name_l'] = member['name_low']
        self.render(template, 
                    tpl_values = tpl_values, 
                    articles = articles, 
                    newest = newest)  
        

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        template = "register.html"
        tpl_values =   {
                'auth'     :   False,
                'title'    :   "REGISTER",
                'name'     :   "",
                'name_l'   :   "",
                'errors'   :   [],}
        self.render(template, tpl_values=tpl_values)

    def post(self):
        db_member = self.application.db['member']
        member = {}

        tpl_values = {
                'auth' : False,
                'title' : "INDEX",
                'name' : "",
                'name_l' : "",
                'errors' : [],}                        

        post_values = ['name','pwd','cpwd','email']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                tpl_values['errors'].append("complete the blanks")
                template = "register.html"
                self.render(template, tpl_values=tpl_values)

        # authentication uname
        UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
        m = re.match(UID_PATT, args['name'])
        if m:
            found = db_member.find_one(
                    {'name_low': args['name'].lower()})
            if found:
                tpl_values['errors'].append("uname exist")
            else:
                member['name'] = args['name']
                member['name_low'] = args['name'].lower()
        else:
            tpl_values['errors'].append("illegal character")

        # authentication password
        if args['pwd'] and (args['pwd'] == args['cpwd']):
            member['pwd'] = hashlib.sha512(args['pwd']).hexdigest()
        else:
            tpl_values['errors'].append("password different")

        # authentication email
        EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
        if args['email']:
            m = re.match(EMAIL_PATT, args['email'].lower())
            if m:
                found = db_member.find_one(
                        {"email": args['email'].lower()})
                if found:
                    tpl_values['errors'].append(
                            "email already being used")
                else:
                    member['email'] = args['email'].lower()
            else:
                tpl_values['errors'].append("illegal email address")
        else:
            tpl_values['errors'].append("no email")

        if tpl_values['errors']:
            template = "register.html"
            self.render(template, tpl_values=tpl_values)
        else:
            member['date'] = datetime.datetime.utcnow()
            member['nid'] = str(db_member.count() + 1)
            member['auth'] = hashlib.sha512(
                    member['name_low'] + member['pwd']).hexdigest()
            self.set_cookie(name="auth", 
                            value=member['auth'], 
                            expires_days=1)
            self.set_cookie(name="nid",      
                            value=member['nid'],   
                            expires_days=1)
            db_member.insert(member)
            self.redirect('/')


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        template = "login.html"
        tpl_values = {
            'auth' : False,
            'title' : "LOGIN",
            'name' : "",
            'name_l' : "",
            'errors' : [],}
        self.render(template, tpl_values=tpl_values)

    def post(self):
        db_member = self.application.db.member
        template = "login.html"
        tpl_values = {
                'auth': False,
                'title': "LOGIN",
                'name': "",
                'name_l': "",
                'errors': [],}

        post_values = ['name','pwd']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                tpl_values['errors'].append("complete the blanks")
                self.render(template, tpl_values=tpl_values)
        
        try:
            member = db_member.find_one(
                    {'name_low':args['name'].lower()})
            if member:
                try:
                    input_auth = hashlib.sha512(
                            args['name'].lower() + 
                            hashlib.sha512(args['pwd']
                            ).hexdigest()).hexdigest()
                    if member['auth'] == input_auth:
                        self.set_cookie(name="auth",
                                value=member['auth'], 
                                expires_days=1)
                        self.set_cookie(name="nid", 
                                value=member['nid'],   
                                expires_days=1)
                        self.redirect('/')
                    else:
                        tpl_values['errors'].append(
                                "error with id or password")
                        self.render(template, tpl_values=tpl_values)
                except:
                    self.render(template, tpl_values=tpl_values)
            else:
                tpl_values['errors'].append("no such user") 
                self.render(template, tpl_values=tpl_values)
        except:
            tpl_values['errors'].append("db error")
            self.render(template, tpl_values=tpl_values)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


class HomeHandler(tornado.web.RequestHandler):
    def get(self, page="index"):
        pages = ('write', 'manage', 'setting', 'index')
        db_member = self.application.db.member
        db_article = self.application.db.article

        template = "home/%s.html" % (page,)

        tpl_values = {
                'auth': False,
                'title': "ANRAN",
                'name': "", # member name
                'name_l': "",} # membet name lowercase

        try:     
            member = CheckAuth(self.get_cookie('auth'))
            if not member:
                self.send_error(401)
            if page in pages:
                tpl_values['auth'] = True
                tpl_values['name'] = member['name']
                tpl_values['name_l'] = member['name_low']
                if (page == "manage"):
                    Cursor = db_article.find(
                        {"author":member['name_low']}).sort("sn",-1)
                    articles = []
                    for a in Cursor:
                        articles.append((a['sn'], a['title']))
                    self.render(template, 
                                tpl_values = tpl_values, 
                                articles = articles)
                    self.finish()
                self.render(template, 
                            tpl_values = tpl_values)
            else:
                self.send_error(404) 
                self.finish()   
        except:
            pass
    def post(self):
        try:
            target = self.get_argument("o")
            if target == 'del':
                article_sn = self.get_argument("sn")
                db_article = self.application.db.article
                member = CheckAuth(self.get_cookie('auth'))
                if member:
                    db_article.remove({'sn': article_sn})
                else:
                    self.send_error('403')
        except:
            pass

    


class UserHandler(tornado.web.RequestHandler):
    def get(self,arg):
        self.write("hello" + arg)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


