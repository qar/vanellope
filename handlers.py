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

import tornado.web
import tornado.escape

import markdown
import settings

from page302.utility import *
from page302.security import CheckAuth


class ArticleHandler(tornado.web.RequestHandler):
    def get(self, article_sn):
        db_article = self.application.db.article
        db_member = self.application.db.member

        article = db_article.find_one({'sn': article_sn})
        author = db_member.find_one({'name_low': article['author'].lower() })

        member = CheckAuth(self.get_cookie('auth'))

        template = "article.html"
        try:
            option = self.get_argument('m')
        except:
            option = None
        if option == 'modify':
            template = "home/edit.html"
            title = "Edit"
        else:
            title ="page302"
            article['heat'] += 1
            db_article.save(article)
            md = markdown.Markdown(safe_mode = "escape")
            article['body'] = md.convert(article['body'])
        self.render(template, 
                    member = member,
                    title = title,
                    author = author, 
                    article = article)
        
    def post(self):
        db_article = self.application.db.article
        db_member = self.application.db.member

        post_values = ['intro-img', 'title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass

        article = { 
                'sn':  str(int(time.time())),
                'statue': 0,
                'img': None,
                'author': None,
                'heat': 0,
                'title': None,
                'brief': None,
                'body': None,
                'date': datetime.datetime.utcnow(),
                'review': datetime.datetime.utcnow(),
        }

        # deal with uploaded file 
        upload = self.request.files['intro-img'][0]
        md5 = hashlib.md5(upload['body']).hexdigest()
        fpath = ('static/img/article/intro-%s.%s' % 
                (md5, upload['filename'].split('.')[-1]))
        fp = os.path.join(os.path.dirname(__file__), fpath)
        pic =  open(fp, 'wb')
        pic.write(upload['body'])
        pic.close()

        article['img'] = fpath
        article['title'] = args['title']
        article['brief'] = args['brief']
        article['body'] = args['content']
        try:     
            cookie_auth = self.get_cookie("auth")
            member = CheckAuth(self.get_cookie('auth'))
            if member:
                article['author'] = member['name']
                db_article.insert(article)
                self.redirect('/')
            else:
                send_error(401)
        except:
            logging.warning("Unexpecting Error")        


class UpdateHandler(tornado.web.RequestHandler):
    def post(self, article_id):
        member = CheckAuth(self.get_cookie('auth'))
        db_article = self.application.db.article
        article = db_article.find_one({"sn":article_id})
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                continue
        if member:
            article['title']  = args['title']
            article['brief'] = args['brief']
            article['body'] = args['content']
            article['review'] = datetime.datetime.utcnow()
            db_article.update({"sn":article_id}, article)
            self.redirect("/archive/%s" % article_id)
        else:
            self.send_error(403)



class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        template = "register.html"
        self.render(template, 
                    title = 'Register',
                    errors = None,
                    member = None)

    def post(self):
        db_member = self.application.db['member']
        template = "register.html"
        title = "Register"
        errors = []
        member = {}                       

        post_values = ['name','pwd','cpwd','email']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                errors.append("complete the blanks")
                self.render(template, title = title, 
                            member = member, errors = errors)

        # authentication uname
        UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
        m = re.match(UID_PATT, args['name'])
        if m:
            found = db_member.find_one(
                    {'name_low': args['name'].lower()})
            if found:
                errors.append("uname exist")
            else:
                member['name'] = args['name']
                member['name_low'] = args['name'].lower()
        else:
            errors.append("illegal character")

        # authentication password
        if args['pwd'] and (args['pwd'] == args['cpwd']):
            member['pwd'] = hashlib.sha512(args['pwd']).hexdigest()
        else:
            errors.append("password different")

        # authentication email
        EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
        if args['email']:
            match = re.match(EMAIL_PATT, args['email'].lower())
            if match:
                exist = db_member.find_one({"email": args['email'].lower()})
                if exist:
                    errors.append("email already being used")
                else:
                    member['email'] = args['email'].lower()
            else:
                errors.append("illegal email address")
        else:
            errors.append("no email")

        if errors:
            template = "register.html"
            self.render(template, title=title, 
                        errors = errors, member = None)
        else:
            member['date'] = datetime.datetime.utcnow()
            member['nid'] = str(db_member.count() + 1)
            member['auth'] = hashlib.sha512(member['name_low'] + 
                             member['pwd']).hexdigest()
            member['avatar'] = Avatar(member['email'])
            self.set_cookie(name="auth", 
                            value=member['auth'], 
                            expires_days = 365)
            self.set_cookie(name="nid",      
                            value=member['nid'],   
                            expires_days = 365)
            db_member.insert(member)
            self.redirect('/')


