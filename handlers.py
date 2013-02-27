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
import json
import pymongo

import tornado.web
import tornado.escape

import markdown
import settings

from article import Article
from member import Member
from page302.utility import *
from page302.security import CheckAuth


class ArticleHandler(tornado.web.RequestHandler):
    def __init__(self, *request, **kwargs):
        super(ArticleHandler,self).__init__(request[0], request[1])
        self.db_article = self.application.db.article
        self.db_member = self.application.db.member
        self.db_comment = self.application.db.comment

    def get(self, article_sn):
        template = "article.html"
        # check whether member logged in
        master = CheckAuth(self.get_cookie('auth'))

        article = self.db_article.find_one({'sn': int(article_sn)})
        author = self.db_member.find_one({'uid': article['author'] })
        comments_cursor = self.db_comment.find({
                          'article_id': int(article_sn)}).sort('date',1)
        comments = []
        for comment in comments_cursor:
            comment['date'] += datetime.timedelta(hours=8)
            comment['date'] = comment['date'].strftime("%Y-%m-%d %H:%M")
            comments.append(comment)

        article['heat'] += 1
        self.db_article.save(article)

        #get previous and next page link
        try:
            pre = self.db_article.find({'sn': {'$lt': article['sn']}}).sort('sn', -1)
            pre = pre[0]['sn']
        except:
            pre = None
        try:
            fol = self.db_article.find({'sn': {'$gt': article['sn']}})
            fol = fol[0]['sn']
        except:
            fol = None

        md = markdown.Markdown(safe_mode = "escape")
        article['body'] = md.convert(article['body'])
        article['date'] += datetime.timedelta(hours=8)
        article['date'] = article['date'].strftime("%Y-%m-%d %H:%M")
        article['review'] += datetime.timedelta(hours=8)
        article['review'] = article['review'].strftime("%Y-%m-%d %H:%M")

        self.render(template, 
                    pre = pre,
                    fol = fol,
                    master = master,
                    comments = comments, 
                    title = article['title'],
                    author = author, 
                    article = article)
        
    def post(self):
        self.db_article = self.application.db.article
        self.db_member = self.application.db.member

        # get post arguments
        post_values = ['intro-img', 'title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass

        article = Article()
        article.set_title(args['title'])
        article.set_brief(args['brief'])
        article.set_content(args['content'])
        article.set_avatar(self.__save_uploaded_avatar())

        try:     
            cookie_auth = self.get_cookie("auth")
            master = CheckAuth(self.get_cookie('auth'))
            if master:
                article.set_author(master['uid'])
                article.save()
                self.redirect('/')
            else:
                send_error(401)
        except:
            logging.warning("Unexpecting Error")

    def __save_uploaded_avatar(self, arg="intro-img"):
        # save uploaded file's binary data on local storage.
        # data specified by "arg", default value is "intro-img"
        # when file saved return it's relative link, aka the "url".
        # if no data with request use default link specified by settings.py file.
        try:
            uploaded = self.request.files[arg][0]
            file_md5 = hashlib.md5(uploaded['body']).hexdigest()
            file_ext = uploaded['filename'].split('.')[-1]
            file_name = ("intro-%f-%s.%s" % (file_md5, time.time(), file_ext))
            url = os.path.join("/", 
                               os.path.basename(settings.STATIC_PATH),
                               os.path.basename(settings.IMAGE_PATH),
                               os.path.basename(settings.ARTICLE_AVATAR_PATH),
                               file_name)
            fp = os.path.join(settings.ARTICLE_AVATAR_PATH, file_name)
            pic =  open(fp, 'wb')
            pic.write(uploaded['body'])
            pic.close()
        except:
            url = settings.DEFAULE_ARTICLE_AVATAR
        return url


class ArticleUpdateHandler(tornado.web.RequestHandler):
    def __init__(self, *request, **kwargs):
        super(ArticleUpdateHandler,self).__init__(request[0], request[1])
        self.db_article = self.application.db.article
        self.db_member = self.application.db.member

    def get(self, article_sn):
        master = CheckAuth(self.get_cookie('auth'))
        template = "home/edit.html"
        article = self.db_article.find_one({'sn': int(article_sn)})
        author = self.db_member.find_one({'_id': article['author']})

        self.render(template, 
                    master = master,
                    title = "Edit",
                    author = author,
                    article = article)

    def post(self, article_id):
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                continue

        master = CheckAuth(self.get_cookie('auth'))
        article = self.db_article.find_one({"sn":int(article_id)})
        
        if master:
            article['title']  = args['title']
            article['brief'] = args['brief']
            article['body'] = args['content']
            article['review'] = datetime.datetime.utcnow()
            self.db_article.update({"sn":int(article_id)}, article)
            self.redirect("/article/%s" % article_id)
        else:
            self.send_error(403)

class CommentHandler(tornado.web.RequestHandler):
    def __init__(self, *request, **kwargs):
        super(CommentHandler,self).__init__(request[0], request[1])
        self.db_article = self.application.db.article
        self.db_comment = self.application.db.comment

    def get(self):
        pass

    def post(self, article_sn):
        master = CheckAuth(self.get_cookie('auth'))

        cmt = self.get_argument('comment')
        #comment database schema
        comment = {
            'member_name':None,
            'member_avatar':None,
            'member_id': None,
            'article_id':None,
            'comment':None,
            'date':None,
        }

        if master:
            comment['member_name'] = master['name']
            comment['member_avatar'] = master['avatar']
            comment['member_id'] = master['uid']
            comment['article_id'] = int(article_sn)
            comment['comment'] = cmt
            comment['date'] = datetime.datetime.utcnow()
            self.db_comment.insert(comment)
            self.redirect("/article/%s" % article_sn)
        else:
            self.send_error(403)


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        template = "register.html"
        self.render(template, 
                    title = 'Register',
                    errors = None,
                    master = None)

    def post(self):
        self.db_member = self.application.db['member']
        template = "register.html"
        title = "Register"
        errors = []

        member = Member()                       

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
        if re.match(UID_PATT, args['name']):
            found = member.check_name(args['name'])
            if found:
                errors.append("uname exist")
            else:
                member.set_name(args['name'])
        else:
            errors.append("illegal character")

        # authentication password
        if args['pwd'] and (args['pwd'] == args['cpwd']):
            member.set_pwd(hashlib.sha512(args['pwd']).hexdigest())
        else:
            errors.append("password different")

        # authentication email
        EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'
        if args['email']:
            if re.match(EMAIL_PATT, args['email'].lower()):
                if member.check_email(args['email'].lower()):
                    # email being using
                    errors.append("email already being used")
                else:
                    member.set_email(args['email'].lower())
            else:
                errors.append("illegal email address")
        else:
            errors.append("no email")

        if errors:
            template = "register.html"
            self.render(template, title=title, 
                        errors = errors, member = None)
        else:
            member.set_auth(hashlib.sha512(member.template['name']+ 
                             member.template['pwd']).hexdigest())
            member.set_avatar(Avatar(member.template['email']))
            self.set_cookie(name="auth", 
                            value=member.template['auth'], 
                            expires_days = 365)
            member.save()
            self.redirect('/')


