# /usr/bin/env python
# coding=utf-8

import datetime
import json
import tornado.web
import logging

from markdown import markdown

from vanellope import da
from vanellope import db
from vanellope import constant as cst

from vanellope.model import Article
from vanellope.model import Member

from vanellope.handlers import BaseHandler


class ArticleHandler(BaseHandler):
    def get(self, article_sn):
        article = da.get_article_by_sn(int(article_sn)) # wrappered
        if not article:
            self.send_error(404)
            self.finish()

        author = da.get_author(article.author).pack
        comments = da.get_comment_list_by_sn(article.sn)

        da.heat_article_by_sn(int(article_sn))
        adjoins = da.find_adjoins(article.date)
        tpl = dict(
            sn = article.sn,
            title = article.title,
            body = article.html,
            brief = article.sub_title,
            date = article.date + datetime.timedelta(hours=8),
            review = article.review + datetime.timedelta(hours=8),
            heat = article.heat,
        )
        tpl['date'] = tpl['date'].strftime("%Y-%m-%d %H:%M") 
        tpl['review'] = tpl['review'].strftime("%Y-%m-%d %H:%M") 
        self.render("article.html", 
                    pre = adjoins[0],
                    fol = adjoins[1],
                    master = self.get_current_user(),
                    comments = comments, 
                    title = article.title,
                    author = author, 
                    article = tpl)

    #create article
    @tornado.web.authenticated
    def post(self):
        article = Article()
        # get post values
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)
  
        article.set_sn()
        article.set_title(args['title'])
        article.set_sub_title(args['brief'])
        article.set_markdown(args['content'])
        article.set_html(markdown(args['content'], 
                        ['fenced_code', 'codehilite'], 
                        safe_mode= "escape"))

        master = Member(self.get_current_user())
        article.set_author(master.uid)
        article.put()
        self.redirect('/')

    @tornado.web.authenticated
    def delete(self, article_sn):
        article = da.get_article_by_sn(int(article_sn))
        if article.status == cst.DELETED:
            # Remove related data, like comments
            # Remove article that already markded "deleted".
            article.remove()
            da.remove_comments_with_article(int(article_sn))
        else:
            # Just mark the article "deleted", not remove it.
            article.set_status(cst.DELETED)
            article.put()
        self.finish()


class ArticleUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, sn):
        article = da.get_article_by_sn(int(sn)) # a wrapper
        author = da.get_author(article.author) # a wrapper

        self.render("edit.html", 
                    master = self.get_current_user(),
                    title = "Edit",
                    author = author.pack,
                    article = article.pack)

    @tornado.web.authenticated
    def post(self, sn):
        article = Article()
        # get post values
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)
        master = self.get_current_user()

        article = da.get_article_by_sn(int(sn))
        article.set_title(args['title'])
        article.set_sub_title(args['brief'])
        article.set_markdown(args['content'])
        article.set_html(markdown(args['content'], 
                        ['fenced_code', 'codehilite'], 
                        safe_mode= "escape"))

        article.set_review()
        article.put()
        self.redirect("/article/%s" % sn)


# Ajax call handler
class RecoverHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, article_sn):
        article = db.article.find_one({"sn": int(article_sn)})
        article['status'] = cst.NORMAL
        db.article.save(article)
        self.set_status(200)
        return True
   

# Ajax call handler
class PagesHandler(BaseHandler):
    def get(self, page=1):
        uname = self.get_argument("name", None)
        page = int(page)
        master = self.get_current_user()
        if not uname:
            if master:
                author = master['uid']
            else:
                self.set_status(404)
                self.finish()
        else:
            author = db.member.find_one({"name":uname})['uid']
        t = split_pages(author=author, page=page)
        json_file = json.dumps(t[2])
        self.finish(json_file)


class HotestHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, N=10):
        # N articles to be returned
        articles = db.article.find({"status":cst.NORMAL}).sort("heat", -1).limit(int(N))
        return_value = [dict(title=i['title'], sn=i['sn']) for i in articles] 
        self.finish(json.dumps(return_value))

