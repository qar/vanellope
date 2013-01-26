#! /usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import os.path
import hashlib
import pymongo
import re
import datetime

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",                  IndexHandler),
            (r"/register",          RegisterHandler),
            (r"/archive/([0-9]+.*)",ArchiveHandler),
            (r"/article",           ArticleHandler),
            (r"/home",              HomeHandler),
            (r"/home/(.*)",         HomeHandler),
            (r"/u/(.*)",            UserHandler),
            (r"/login",             LoginHandler),
            (r"/logout",            LogoutHandler),
            (r"/test",              TestHandler),]
        
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "tpl"),
            debug = True)

        conn = pymongo.Connection('localhost',27017)
        self.db  = conn['page302']

        tornado.web.Application.__init__(self, handlers, **settings)

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.request.arguments
        self.write('hello, %s' % name)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        db_member     =   self.application.db.member
        template    =   "index.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "INDEX",
            'name'     :   "",
            'name_l'   :   "",}

        try:     
            cookie_auth =   self.get_cookie("auth")
            #cookie_id   =   self.get_cookie("id")
            member        =   db_member.find_one({'auth':  cookie_auth})
            if member:
                tpl_values['auth']   =   True
                tpl_values['name']   =   member['name']
                tpl_values['name_l'] =   member['name_low']  
        except:
            pass
        self.render(template, tpl_values=tpl_values)


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        template    =   "register.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "REGISTER",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}

        self.render(template, tpl_values=tpl_values)

    def post(self):
        db_member     =    self.application.db['member']
        member       =    {}

        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "INDEX",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}                        

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
            found = db_member.find_one({'name_low': args['name'].lower()})
            if found:
                tpl_values['errors'].append("uname exist")
            else:
                member['name']       = args['name']
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
                found = db_member.find_one({"email": args['email'].lower()})
                if found:
                    tpl_values['errors'].append("email already being used")
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
            member['auth'] = hashlib.sha512(member['name_low'] + member['pwd']).hexdigest()
            self.set_cookie(name="auth",    value=member['auth'], expires_days=1)
            self.set_cookie(name="nid",      value=member['nid'],   expires_days=1)
            db_member.insert(member)
            self.redirect('/')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        template    =   "login.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "LOGIN",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}
        self.render(template, tpl_values=tpl_values)

    def post(self):
        db_member = self.application.db.member
        template    =   "login.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "LOGIN",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}

        post_values = ['name','pwd']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                tpl_values['errors'].append("complete the blanks")
                self.render(template, tpl_values=tpl_values)
        
        try:
            member = db_member.find_one({'name_low':args['name'].lower()})
            if member:
                try:
                    input_auth = hashlib.sha512(args['name'].lower() + hashlib.sha512(args['pwd']).hexdigest()).hexdigest()
                    if member['auth'] == input_auth:
                        self.set_cookie(name="auth",    value=member['auth'], expires_days=1)
                        self.set_cookie(name="nid",      value=member['nid'],   expires_days=1)
                        self.redirect('/')
                    else:
                        tpl_values['errors'].append("error with id or password")
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
        db_member     =   self.application.db.member
        db_article  =   self.application.db.article
        template    =   "home/%s.html" % (page,)
        print page
        tpl_values  =   {
                'auth'     :   False,
                'title'    :   "ANRAN",
                'name'     :   "",
                'name_l'   :   "",}

        try:     
            cookie_auth     =   self.get_cookie("auth")
            member        =   db_member.find_one({'auth':  cookie_auth})
            if not member:
                self.send_error(401)
            if page in pages:
                tpl_values['auth']   =   True
                tpl_values['name']   =   member['name']
                tpl_values['name_l'] =   member['name_low']  
                self.render(template, tpl_values=tpl_values)
            else:
                self.send_error(404)    
        except:
            self.send_error(500)

class ArchiveHandler(tornado.web.RequestHandler):
    def get(self, archive_sn):
        db_member = self.application.db.member

        template    =   "archive.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "SN=" + archive_sn,
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}      

        try:     
            cookie_auth =   self.get_cookie("auth")
            #cookie_id   =   self.get_cookie("id")
            member        =   db_member.find_one({'auth':  cookie_auth})
            if member:
                tpl_values['auth']   =   True
                tpl_values['name']   =   member['name']
                tpl_values['name_l'] =   member['name_low']  
        except:
            pass
        self.render(template, tpl_values=tpl_values)

class ArticleHandler(tornado.web.RequestHandler):
    def post(self):
        db_article = self.application.db.article
        db_member = self.application.db.member

        article = {
            'sn'        :   None,   # seril number
            'title'     :   '',
            'subtitle'  :   '',
            'content'   :   '',
            'author'    :   '',
            'heat'      :   0,
            'link'      :   {}, # name are captions of the related link
            'img'       :   [], #imgs[0] should be intro-image
        }
        post_values = ['title','subtitle','intro-img','imgs','links']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass
        article['sn'] = str(db_article.count())
        article['title'] = args['title']
        article['subtitle'] = args['subtitle']
        upload_file = self.request.files['intro-img'][0]
        fpath = 'static/img/article/%s-intro.%s' % (article['sn'], upload_file['filename'].split('.')[-1])
        fp =  open(fpath, 'wb')
        fp.write(upload_file['body'])
        fp.close()
        try:     
            cookie_auth =   self.get_cookie("auth")
            #cookie_id   =   self.get_cookie("nid")
            member        =   db_member.find_one({'auth':  cookie_auth})
            if member:
                article['author'] =   member['name_low']  
                self.write("hello")
        except:
            pass
        pass

class UserHandler(tornado.web.RequestHandler):
    def get(self,arg):
        self.write("hello" + arg)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


