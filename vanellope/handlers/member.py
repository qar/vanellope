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

        # I add a method to BaseHandler to replace this below:
        #m = Member(self.get_current_user())
        #master = dict(
        #    color = m.color,
        #    name = m.name,
        #)
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
        #
        # Message Receiver
        m = Member(self.get_current_user()) # wrapped 
        msg = self.get_argument("message", None)
        message = Message() # initialize a message object
        try:
            message.set_sender(m.uid) # Use ID as identifier
            message.set_receiver(int(she)) # May be it is a girl
            message.set_body(msg) # The main content
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
        #
        #m = Member(self.get_current_user())
        #master = dict(
        #    uid = m.uid,
        #    color = m.color,            
        #    avatar_large = m.avatar_large,
        #    brief = m.brief,
        #    name = m.name,
        #    email = m.email,
        #)
        #my_msg = da.get_msg_by_receiver(master['uid'])

        master = self.master()
        #msgs = da.get_new_messages(master['uid'])
        msgs = da.my_all_messages(master['uid'])
        member = self.member(1)
        
        #try:
        #    peer = [master['uid'], member['uid']]
        #except TypeError:
        #    print "no contacter"
        #msgs = da.get_messages_by_peer(peer.sort())
        #print msgs
        self.render("message.html",
                    title = "Message",
                    master = master,
                    member = member,
                    messages = msgs)




class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, html="home"):
        # Login User Information
        # I add a method to BaseHandler to replace this below:
        #m = Member(self.get_current_user())
        #master = dict(
        #    uid = m.uid,
        #    color = m.color,            
        #    avatar_large = m.avatar_large,
        #    brief = m.brief,
        #    name = m.name,
        #    email = m.email,
        #)
        master = self.master()
        
        htmls = ('write', 'deleted', 'home', 'message') # Available templates
        if html in htmls:
            template = ("%s.html" % html) # Template Selector
        else:
            self.send_error(404)
            self.finish()

        # Articles pages slicing
        page = self.get_argument("p", 1)
        
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
            d = da.split_pages(author=master['uid'], 
                               status=cst.NORMAL,
                               page=page,)
            self.render(template, 
                        title="Home",
                        errors=None,                        
                        master = master,
                        total = d['total'],
                        pages = d['pages'],
                        articles = d['articles'])
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