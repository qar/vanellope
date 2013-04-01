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

import tornado.web

from vanellope import da
from vanellope import db

from vanellope import Mail
from vanellope import regex
from vanellope import constant as cst

from vanellope.model import Member
from vanellope.model import Article
from vanellope.model import Message
from vanellope.handlers import BaseHandler


class MemberHandler(BaseHandler):
    # UTL: /member/USERID
    # Member main information display
    #
    def get(self, uid):
        master = self.master()

        page = self.get_argument("p", 1)
        author = Member(da.get_member_by_uid(uid))

        d = da.split_pages(author=author.uid, page=page)

        if author.uid is None: # no such user, wrong url
            self.send_error(404)
            self.finish()
        elif master['uid'] == author.uid: # user is logined
            self.redirect("/home")
            self.finish()
        
        # this is what we expected
        member = dict(
            avatar_large = author.avatar_large,
            brief = author.brief,
            name = author.name,
        )

        self.render("member.html",
                    title = member['name'],
                    articles = d['articles'],
                    member = member,
                    pages = d['pages'],
                    total = d['total'],
                    master = master) 

    @tornado.web.authenticated
    def post(self, she):
        # Ajax call: receive and store message
        m = Member(self.get_current_user()) # Message Sender 
        msg = self.get_argument("message", None) # Message
        message = Message() # initialize a message object
        try:
            message.set_sender(m.uid) # Use ID as identifier
            message.set_receiver(int(she)) # Message Receiver
            message.set_body(msg) 
            message.put()
            self.finish()
        except TypeError:
            pass
        except ValueError:
            pass
        self.finish() # If error happens, this will end request

class MessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        master = self.master()

        if self.is_ajax():
            pass

        
        msgs = da.my_all_messages(master['uid'])
        #member = self.member(1)

        self.render("message.html",
                    title = "Message",
                    master = master,
                    #member = member,
                    messages = msgs)


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, html="home"):
        master = self.master()
        
        htmls = ('write', 'deleted', 'home', 'message') # Available templates
        if html in htmls:
            template = ("%s.html" % html) # Template Selector
        else:
            self.send_error(404)
            self.finish()

        # Articles pages slicing
        page = self.get_argument("p", 1)
        _type = self.get_argument("type", "post")
        
        if(html == "deleted"):  # aka. the trash bucket
            d = da.split_pages(author=master['uid'], 
                               status=cst.DELETED,
                               page=page)
            self.render(template, 
                        title = '回收站', 
                        master = master,
                        errors=None,                    
                        pages = d['pages'],    
                        articles = d['articles']
                        )
        elif html == "home":
            news = da.get_new_messages(master['uid'])
            d = da.split_pages(author=master['uid'], 
                               status=cst.NORMAL,
                               page=page,
                               _type=_type)
            self.render(template, 
                        title="Home",
                        errors=None,
                        type=_type,                        
                        master = master,
                        total = d['total'],
                        pages = d['pages'],
                        articles = d['articles'],
                        messages = news)
        elif html == "write":
            self.render(template,
                        title=u"撰写",
                        master=master)
        elif html == "message":

            self.render("message.html",
                        title = "Message",
                        master = master)





class BriefHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        master = Member(self.get_current_user()) # wrapped
        brief = master.brief
        self.finish(json.dumps(brief))

    @tornado.web.authenticated
    def post(self):
        master = Member(self.get_current_user()) # wrapped
        brief = self.get_argument('brief', default=None)
        master.set_brief(brief)
        master.put()
        self.finish()


                      
class EmailHandler(BaseHandler):
    # ajax call
    @tornado.web.authenticated
    def get(self):
        master = self.get_current_user()
        self.write(master['email'])
        self.flush()
        self.finish()

    # ajax call
    # Should return a json array
    @tornado.web.authenticated
    def post(self):
        errors = []
        email = self.get_argument("email", None)
        master = Member(self.get_current_user()) # wrapped
        if not master.verified:
            errors.append(u"你现在的邮箱还没有通过验证，暂时不能更换邮箱")
        else:
            try:
                master.set_email(email)
                master.verify()
                master.put()
            except exception.PatternMatchError:
                errors.append(u"请检查邮箱的格式是否正确")
            except exception.DupKeyError:
                errors.append(u"邮箱已被使用")                
            
        if len(errors) > 0:
            self.finish(json.dumps(errors))
        else:
            self.finish(json.dumps(True))