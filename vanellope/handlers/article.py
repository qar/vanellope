# /usr/bin/env python
# coding=utf-8

import datetime
import json
import tornado.web
import logging
from markdown import markdown

from vanellope.model import Article
from vanellope import db
from vanellope.handlers import BaseHandler

class ArticleHandler(BaseHandler):
    def get(self, sn):
        article = Article().reload(sn)
        if not article:
            self.send_error(404)
            self.finish()

        author = db.member.find_one({'uid': article['author'] })
        cursor = db.comment.find({'article': int(sn)}).sort('date',1)
        comments = []
        for comment in cursor:
            comment['date'] += datetime.timedelta(hours=8)
            comment['date'] = comment['date'].strftime("%Y-%m-%d %H:%M")
            comments.append(comment)

        article['heat'] += 1
        db.article.save(article)

        adjoins = self.find_adjoins(article['date'])

        article['body'] = article['html']
        article['brief'] = article['sub_title']
        article['date'] += datetime.timedelta(hours=8)
        article['date'] = article['date'].strftime("%Y-%m-%d %H:%M")
        article['review'] += datetime.timedelta(hours=8)
        article['review'] = article['review'].strftime("%Y-%m-%d %H:%M")

        self.render("article.html", 
                    pre = adjoins[0],
                    fol = adjoins[1],
                    master = self.get_current_user(),
                    comments = comments, 
                    title = article['title'],
                    author = author, 
                    article = article)

    #create article
    @tornado.web.authenticated
    def post(self):
        article = Article()
        # get post values
        post_values = ['intro-img', 'title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                pass
        print dir(article)
        article.set_title(args['title'])
        article.set_sub_title(args['brief'])
        article.set_markdown(args['content'])
        article.set_html(markdown(args['content'], ['fenced_code', 'codehilite'], safe_mode= "escape"))

        try:     
            master = self.get_current_user()
            article.set_author(master['uid'])
            article.put()
            self.redirect('/')
        except:
            logging.warning("Unexpecting Error")

    @tornado.web.authenticated
    def delete(self, article_sn):
        article = db.article.find_one({"sn": int(article_sn)})
        if article['status'] == "deleted":
            # Remove article that already markded "deleted".
            db.article.remove(article)
        else:
            # Just mark the article "deleted", not remove it.
            article['status'] = "deleted"
            db.article.save(article)
        self.finish()

    def find_adjoins(self, current_date):
        try:
            pre = db.article.find({"status":"normal", 'date':
                {'$lt': current_date}}).sort("date",-1)[0]['sn']
        except:
            pre = None
        try:
            fol = db.article.find({"status":"normal", 'date': 
                {"$gt": current_date}}).sort("date", 1)[0]['sn']
        except:
            fol = None
        return (pre, fol)
        

class ArticleUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, sn):
        article = db.article.find_one({'sn': int(sn)})
        author = db.member.find_one({'uid': article['author']})

        self.render("edit.html", 
                    master = self.get_current_user(),
                    title = "Edit",
                    author = author,
                    article = article)

    @tornado.web.authenticated
    def post(self, sn):
        post_values = ['title', 'brief', 'content']
        args = {}
        for v in post_values:
            try:
                args[v] = self.get_argument(v)
            except:
                continue

        master = self.get_current_user()
        article = db.article.find_one({"sn":int(sn)})
        
        if master:
            article['title']  = args['title']
            article['brief'] = args['brief']
            article['markdown'] = args['content']
            article['html'] = markdown(args['content'], ['fenced_code',  'codehilite'], safe_mode="escape" )
            article['review'] = datetime.datetime.utcnow()
            db.article.update({"sn":int(sn)}, article)
            self.redirect("/article/%s" % sn)
        else:
            self.send_error(403)    

class RecoverHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, article_sn):
        # Ajax Call:
        # recover deleted article
        #
        article = db.article.find_one({"sn": int(article_sn)})
        article['status'] = "normal"
        db.article.save(article)
        self.set_status(200)
        return True
   

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
        total = db.article.find({"status":"normal", "author": author}).count()
        articles_per_page = 10
        skip = (int(page) - 1)*articles_per_page
        if int(page) > 0:
            if total > skip:
                articles = db.article.find({"status":"normal", "author":author}).skip(skip).sort("date", -1)
                return_value = [dict(title=i['title'], sn=i['sn']) for i in articles]    
            else:
                return_value = None
        else:
            return_value = None
        json_file = json.dumps(return_value)
        self.finish(json_file)


class HotestHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, N=10):
        # N articles to be returned
        articles = db.article.find({"status":"normal"}).sort("heat", -1).limit(int(N))
        return_value = [dict(title=i['title'], sn=i['sn']) for i in articles] 
        self.finish(json.dumps(return_value))

