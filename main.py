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
            (r"/archive/([0-9]+)",  ArchiveHandler),
            (r"/archive",           ArchiveHandler),
            (r"/home/([a-z]*)",     HomeHandler),
            (r"/u/(.*)",            UserHandler),
            (r"/login",             LoginHandler),
            (r"/logout",            LogoutHandler),]
        
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "tpl"),
            debug = True)

        conn = pymongo.Connection('localhost',27017)
        self.db  = conn['page302']

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        db_user     =   self.application.db['user']
        template    =   "index.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "INDEX",
            'name'     :   "",
            'name_l'   :   "",}

        try:     
            cookie_auth =   self.get_cookie("auth")
            cookie_id   =   self.get_cookie("id")
            user        =   db_user.find_one({'id':  cookie_id})
            if user:
                if cookie_auth == user['auth']:
                    tpl_values['auth']   =   True
                    tpl_values['name']   =   user['uname']
                    tpl_values['name_l'] =   user['uname_lower']  
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
        db_user     =    self.application.db['user']
        user        =    {}

        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "INDEX",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}

        post_values = ['uname','pwd','cpwd','email']
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
        m = re.match(UID_PATT, args['uname'])
        if m:
            found = db_user.find_one({'uname_lower': args['uname'].lower()})
            if found:
                tpl_values['errors'].append("uname exist")
            else:
                user['uname']       = args['uname']
                user['uname_lower'] = args['uname'].lower()
        else:
            tpl_values['errors'].append("illegal character")

        # authentication password
        if args['pwd'] and (args['pwd'] == args['cpwd']):
            user['pwd'] = hashlib.sha512(args['pwd']).hexdigest()
        else:
            tpl_values['errors'].append("password different")


        # authentication email
        EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
        if args['email']:
            m = re.match(EMAIL_PATT, args['email'].lower())
            if m:
                found = db_user.find_one({"email": args['email'].lower()})
                if found:
                    tpl_values['errors'].append("email already being used")
                else:
                    user['email'] = args['email'].lower()
            else:
                tpl_values['errors'].append("illegal email address")
        else:
            tpl_values['errors'].append("no email")

        if tpl_values['errors']:
            template = "register.html"
            self.render(template, tpl_values=tpl_values)
        else:
            user['date'] = datetime.datetime.utcnow()
            user['id'] = str(db_user.count() + 1)
            user['auth'] = hashlib.sha512(user['uname_lower'] + user['pwd']).hexdigest()
            self.set_cookie(name="auth",    value=user['auth'], expires_days=1)
            self.set_cookie(name="id",      value=user['id'],   expires_days=1)
            db_user.insert(user)
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
        db_user = self.application.db.user
        template    =   "login.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "LOGIN",
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}

        post_values = ['uname','pwd']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                tpl_values['errors'].append("complete the blanks")
                self.render(template, tpl_values=tpl_values)
        
        try:
            user = db_user.find_one({'uname_lower':args['uname'].lower()})
            if user:
                try:
                    input_auth = hashlib.sha512(args['uname'].lower() + hashlib.sha512(args['pwd']).hexdigest()).hexdigest()
                    if user['auth'] == input_auth:
                        self.set_cookie(name="auth",    value=user['auth'], expires_days=1)
                        self.set_cookie(name="id",      value=user['id'],   expires_days=1)
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
    def get(self, section):
        db_user     =   self.application.db['user']
        template    =   "home/%s.html" % section
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "ANRAN",
            'name'     :   "",
            'name_l'   :   "",}

        try:     
            cookie_auth =   self.get_cookie("auth")
            cookie_id   =   self.get_cookie("id")
            user        =   db_user.find_one({'id':  cookie_id})
            if user:
                if cookie_auth == user['auth']:
                    tpl_values['auth']   =   True
                    tpl_values['name']   =   user['uname']
                    tpl_values['name_l'] =   user['uname_lower']  
                    self.render(template, tpl_values=tpl_values)
            else:
                self.set_status(404)
                self.write('you have not authorized')
        except:
            pass
       

class ArchiveHandler(tornado.web.RequestHandler):
    def get(self, archive_sn):
        db_user = self.application.db.user

        template    =   "archive.html"
        tpl_values  =   {
            'auth'     :   False,
            'title'    :   "SN=" + archive_sn,
            'name'     :   "",
            'name_l'   :   "",
            'errors'   :   [],}      

        try:     
            cookie_auth =   self.get_cookie("auth")
            cookie_id   =   self.get_cookie("id")
            user        =   db_user.find_one({'id':  cookie_id})
            if user:
                if cookie_auth == user['auth']:
                    tpl_values['auth']   =   True
                    tpl_values['name']   =   user['uname']
                    tpl_values['name_l'] =   user['uname_lower']  
        except:
            pass
        self.render(template, tpl_values=tpl_values)

    def post(self):
        db_arhive = self.application.db.arhive 
        db_user = self.application.db.user  

        archive = {
            'sn'        :   None,   # seril number
            'title'     :   '',
            'subtitle'  :   '',
            'author'    :   '',
            'heat'      :   0,
            'links'     :   [],
            'imgs'      :   [], #imgs[0] should be intro-image
        }
        post_values = ['title','subtitle','intro-img','imgs','links']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass
        archive['sn'] = str(db_arhive.count())
        archive['title'] = args['title']
        archive['subtitle'] = args['subtitle']
        upload_file = self.request.files['intro-img']
        print upload_file
        try:     
            cookie_auth =   self.get_cookie("auth")
            cookie_id   =   self.get_cookie("id")
            user        =   db_user.find_one({'id':  cookie_id})
            if user:
                if cookie_auth == user['auth']:
                    archive['author'] =   user['uname_lower']  
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


