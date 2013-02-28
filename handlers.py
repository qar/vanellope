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
from member import Member, CheckAuth, Avatar
from comment import Comment


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

        try:
            option = self.get_argument("option")
            if option == "deleted" and master:
                self.delete_article(article_sn)
                self.set_status(200)
                self.finish()
        except:
            pass

        article = self.db_article.find_one({"status": "normal", 'sn': int(article_sn)})
        if not article:
            self.send_error(404)
            self.finish()

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

        adjoins = self.find_adjoins(article['date'])

        md = markdown.Markdown(safe_mode = "escape")
        article['body'] = md.convert(article['body'])
        article['date'] += datetime.timedelta(hours=8)
        article['date'] = article['date'].strftime("%Y-%m-%d %H:%M")
        article['review'] += datetime.timedelta(hours=8)
        article['review'] = article['review'].strftime("%Y-%m-%d %H:%M")

        self.render(template, 
                    pre = adjoins[0],
                    fol = adjoins[1],
                    master = master,
                    comments = comments, 
                    title = article['title'],
                    author = author, 
                    article = article)
        
    def post(self):
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
        article.set_avatar(self.save_uploaded_avatar())

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

    def find_adjoins(self, current_date):
        try:
            pre = self.db_article.find({'date':
                {'$lt': current_date}}).sort("date",-1)[0]['sn']
        except:
            pre = None
        try:
            fol = self.db_article.find({'date': 
                {"$gt": current_date}}).sort("date", 1)[0]['sn']
        except:
            fol = None
        return (pre, fol)

    def save_uploaded_avatar(self, arg="intro-img"):
        # save uploaded file's binary data on local storage.
        # data specified by "arg", default value is "intro-img"
        # when file saved return it's relative link, aka the "url".
        # if no data with request use default link specified by settings.py file.
        try:
            uploaded = self.request.files[arg][0]
            file_md5 = hashlib.md5(uploaded['body']).hexdigest()
            file_ext = uploaded['filename'].split('.')[-1]
            file_name = ("intro-%f-%s.%s" % (time.time(), file_md5, file_ext))
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

    def delete_article(self, article_sn):
        self.db_article.update({"sn":article_sn}, {"$set":{"status":"deleted"}})

    def recover_article(self, article_sn):
        self.db_article.update({"sn":article_sn}, {"$set":{"status":"normal"}})

    def preserve_article(self, article_sn):
        self.db_article.update({"sn":article_sn}, {"$set":{"status":"preserved"}})


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
    def post(self, article_sn):
        master = CheckAuth(self.get_cookie('auth'))
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


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        template = "register.html"
        self.render(template, 
                    title = 'Register',
                    errors = None,
                    master = None)

    def post(self):
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

        # check and set 'name'. 
        # If anything went wrong error messages list returned
        errors += member.check_name(args['name'])

        if args['pwd'] and (args['pwd'] == args['cpwd']):
            member.set_pwd(args['pwd'])
        else:
            errors.append("password different")

        # authentication email
        if args['email']:
            # check and set 'email'. 
            # If anything went wrong error messages list returned
            errors += member.check_email(args['email'])
        else:
            errors.append("no email")

        if errors:
            self.render("register.html", #template file
                        title = "Register", # web page title
                        errors = errors,    
                        member = None)
        else:
            member.save()
            self.set_cookie(name="auth", 
                            value=member.get_auth(), 
                            expires_days = 365)
            self.redirect('/')


