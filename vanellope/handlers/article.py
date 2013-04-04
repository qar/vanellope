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
from vanellope.model import Comment
from vanellope.handlers import BaseHandler


class ArticleHandler(BaseHandler):
    # URL: /article/ARTICLE_SN
    def get(self, article_sn):
        article = da.get_article_by_sn(int(article_sn))
        if not article or article['status'] == cst.DELETED:
            self.send_error(404)
            self.finish()
        else:
            article = Article(article) # wrapped

        article = dict(
            sn = article.sn, # usage: widgets/comment.html
            author = article.author,
            title = article.title,
            body = article.html,
            heat = article.heat, # usage: widgets/article-status.html
            date = article.date,
            review = article.review,
        )

        author = self.get_user(uid=article['author'])

        cmts = da.get_comment_list_by_sn(article_sn)
        comments = []
        for cmt in cmts:
            cmt = Comment(cmt)
            comments.append(dict(
                member = cmt.member,
                date = cmt.date,
                floor = cmt.cid,
                body = cmt.body
            ))

        current_user = self.get_current_user()

        da.heat_article_by_sn(int(article_sn)) # increase 'heat' tag then save

        adjoins = da.find_adjoins(article['date'])

        article['date'] = (article['date'] + 
                       datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") 
        article['review'] = (article['review'] + 
                       datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") 

        self.render("article.html", 
                    adjoins = adjoins,
                    master = current_user,
                    comments = comments, 
                    title = article['title'],
                    author = author, 
                    article = article)

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

        current_user = self.get_current_user()
        article.set_author(current_user['uid'])
        article.put()
        self.redirect('/')

    @tornado.web.authenticated
    def delete(self, article_sn):
        # This currently is a ajax call
        # Request URL:/article/ARTICLE
        # Request Method:DELETE
        current_user = self.get_current_user()
        article = Article(da.get_article_by_sn(int(article_sn))) # wrapped
        if current_user['uid'] != article.author:
            self.finish(json.dumps(False))
        else:
            if article.status == cst.DELETED:
                # Remove related data, like comments
                # Remove article that already markded "deleted".
                article.remove()
                da.remove_comments_with_article(int(article_sn))
            else:
                # Just mark the article "deleted", not remove it.
                article.set_status(cst.DELETED)
                article.put()
            self.finish(json.dumps(True))


class ArticleUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, sn):
        t = Article(da.get_article_by_sn(int(sn))) # wrapped
        current_user = self.get_current_user() # wrapped
        article = dict(
            sn = t.sn, # usage: widgets/comment.html
            title = t.title,
            sub_title = t.sub_title,
            markdown = t.markdown,
            author = t.author,
        )
        if article['author'] == current_user['uid']:
            self.render("edit.html", 
                        title = "Edit",
                        master=current_user,
                        article = article)
        else:
            self.send_error(403)
            self.finish()

    @tornado.web.authenticated
    def post(self, sn):
        # get post values
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            # Get nessary argument
            # Use None as default if argument is not supplied
            args[v] = self.get_argument(v, None)

        current_user = self.get_current_user() # wrapped

        article = Article(da.get_article_by_sn(int(sn)))
        
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
        current_user = self.get_current_user()
        if not uname:
            if current_user:
                author = current_user['uid']
            else:
                self.set_status(404)
                self.finish()
        else:
            author = self.get_user(name=uname)
        t = split_pages(author=author['uid'], page=page)
        json_file = json.dumps(t[2])
        self.finish(json_file)


class HotestHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, N=10):
        # N articles to be returned
        articles = db.article.find({"status":cst.NORMAL}).sort("heat", -1).limit(int(N))
        return_value = [dict(title=i['title'], sn=i['sn']) for i in articles] 
        self.finish(json.dumps(return_value))



handlers = [
    (r"/article", ArticleHandler),
    (r"/article/([0-9]+)", ArticleHandler),
    (r"/article/page/([0-9]+)\.json", PagesHandler),
    (r"/article/recover/([0-9]+)", RecoverHandler),
    (r"/update/(.*)", ArticleUpdateHandler),
    (r"/article/hotest/([0-9]+)", HotestHandler),
]