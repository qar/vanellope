#! /usr/bin/env python
# coding=utf-8

import re
import hashlib
import urllib
import urlparse
import datetime
import smtplib
import string
import random
import json
import config


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import tornado.web

from vanellope import db, Mail
from vanellope.handlers import BaseHandler


UID_PATT = r'^[a-zA-Z0-9]{1,16}$'
CSS_COlOR_PATT = r"#[0-9a-fA-F]{6}"
EMAIL_PATT = r'^[a-z0-9\.]+@[a-z0-9]+\.[a-z]{2,4}$'


class MemberHandler(BaseHandler):
    #
    # Member main information display
    #
    def get(self, uname):
        page = self.get_argument("p", 1)
        skip_articles = (int(page) -1 )*10
        author = db.member.find_one({"name_safe": uname})
        articles = db.article.find({"status":"normal",
                                    "author": author['uid']}).sort("date",-1).limit(skip_articles)

        total = db.article.find({"status":"normal", "author": author['uid']}).count()
        pages  = total // 10 + 1
        if total % 10 > 0:
            pages += 1
        master = self.get_current_user()
        if master and master['name_safe'] == uname:
            self.redirect("/home")
        else:
            member = author
        self.render("member.html",
                    title = author['name']+u"专栏",
                    articles = articles,
                    member = member,
                    pages = pages,
                    master = master) 

class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, html="home"):
        htmls = ('write', 'index', 'deleted')

        template = ("%s.html" % html)
        page = self.get_argument("p", 1)
        
        master = self.get_current_user()
        pages = self.count_pages(master['uid'])
        if(html == "deleted"):
            articles = self.deleted_articles(master['uid'])
            self.render(template, 
                        title = '回收站', 
                        master = master,
                        member = master,
                        errors=None,                        
                        articles = articles)
        else:
            articles = self.normal_articles(master['uid'])
            self.render(template, 
                        title="Home",
                        errors=None,                        
                        master = master,
                        pages = pages,
                        member = master,
                        articles = articles)

    @tornado.web.authenticated
    def post(self):
        master = self.get_current_user()
        if master:
            brief = self.get_argument('brief', default=None)
            db.member.update({"uid":master['uid']},{"$set":{"brief":brief}})
            member = db.member.find_one({'uid': master['uid']})
            self.finish(brief)
        else:
            self.send_error(403)
            self.findish()

    def get_author_all_articles(self, owner_id):
        return db.article.find({"author": owner_id}).sort("date", -1)

    def normal_articles(self, owner_id):
        return db.article.find(
                {"author": owner_id, "status":"normal"}).sort("date", -1)

    def deleted_articles(self, owner_id):
        return db.article.find(
                {"author": owner_id, "status":"deleted"}).sort("date", -1)

    def count_pages(self, owner_id=None, p=10, status="normal"):
        # p, articles per page
        p = int(p)
        if owner_id: # one member's
            total = db.article.find(
                {"status":status, "author":owner_id}).count()
        else: # all members'
            total = db.article.find({"status":status}).count()
        pages = total // p + 1 # pages count from 1
        if total % p > 0:      # the last page articles may not equal to 'p' 
            pages += 1 
        return pages
  
  
                      
class EmailHandler(BaseHandler):
    # ajax call
    @tornado.web.authenticated
    def get(self):
        master = self.get_current_user()
        self.write(master['email'])
        self.flush()
        self.finish()

    # ajax call
    def post(self):
        errors = []
        _email = self.get_argument("email", None)
        if re.match(EMAIL_PATT, _email):
            ex = db.member.find_one({"email":_email})
            if not ex:
                master = self.get_current_user()
                master['email'] = _email.lower()
                db.member.save(master)
            else:
                errors.append(u"邮箱已被使用")
        else:
            errors.append(u"请检查邮箱的格式是否正确")
        if len(errors) > 0:
            self.write(json.dumps(errors))
        else:
            self.write(json.dumps(True))
        self.flush()
        self.finish()