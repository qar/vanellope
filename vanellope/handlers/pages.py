# coding=utf-8

import math
import hashlib
import base64
from tornado import web
from tornado.web import authenticated
from vanellope.handlers import BaseHandler
from vanellope import config
from vanellope.handlers import Days


class WelcomePage(BaseHandler):
    def get(self):

        admin = self.user.get_admin_user()

        if admin:
            return self.redirect('/')

        self.render("welcome.html",
                    title=u'Welcome',
                    page=u'welcome')

    def post(self):
        """Signup"""

        admin = self.user.get_admin_user()

        if admin:
            self.set_status(400)
            return self.finish({
                'status': u'error'
            })

        email = self.get_argument('email', None)
        pwd = self.get_argument('pwd', None)
        role = self.get_argument('role', None)

        err = 0
        msg = u'login successfully'

        admin_user = self.user.get_admin_user()
        if role == 'admin' and admin_user:
            err += 1
            msg = u'Admin user exists'

        else:
            password_hash = self.user.create_user({
                "username": "Admin",
                "email": email,
                "password": pwd,
                "role": role
            })

            self.clear_all_cookies()
            cookie = base64.b64encode('Admin:' + password_hash)
            self.set_cookie(name="vanellope",
                            value=cookie,
                            expires_days=90)

            admin_user = self.user.get_admin_user()
            self.settings['admin'] = admin_user

        self.finish({
            'status': u'success',
            'msg': msg
        })


class IndexPage(BaseHandler):
    def get(self):

        ENTRIES_PER_PAGE = config.posts_per_page
        current_page = int(self.get_argument(u'p', 1))

        current_user = self.get_current_user()
        if current_user and current_user['role'] == 'admin':
            drafts = self.posts.get_drafts()
        else:
            drafts = []

        articles = self.posts.find(
            states=['published'],
            limit=ENTRIES_PER_PAGE,
            skip=(current_page - 1) * ENTRIES_PER_PAGE
        )

        total_entries = self.posts.count(states=['published'])

        pages = int(math.floor(total_entries / ENTRIES_PER_PAGE))
        if total_entries > pages * ENTRIES_PER_PAGE:
            pages += 1

        self.render("index.html",
                    title=u'首页 | VANELLOPE',
                    page=u'index',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    pages=pages,
                    drafts=drafts,
                    articles=articles)


class TagsPage(BaseHandler):
    def get(self):
        current_page = int(self.get_argument(u'p', 1))

        self.render("tags.html",
                    title=u'标签 | VANELLOPE',
                    page=u'tags',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1)


class TagPage(BaseHandler):
    def get(self, tag):
        current_page = int(self.get_argument(u'p', 1))

        articles = self.posts.find_posts_with_tag(tag)

        self.render("tag.html",
                    title=u"VANELLOPE | Tag:{0}".format(tag),
                    page=u'tag',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    current_tag=tag,
                    articles=articles)


class ArchivesPage(BaseHandler):
    def get(self):
        self.render('archives.html',
                    title=u'归档 | VANELLOPE',
                    page=u'archives')


class ArchivePage(BaseHandler):
    def get(self, year=u'', month=u'', day=u'12345'):
        if day is None:
            day = u''

        if month is None:
            month = u''

        if year is None:
            year = u''

        current_page = int(self.get_argument(u'p', 1))

        from_date = end_date = None

        if year and month and day:
            from_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, month, day))
                .timezone('UTC')
                .beginning()
            )

            end_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, month, day))
                .timezone('UTC')
                .next_day()
                .beginning()
            )

        elif year and month and not day:
            from_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, month, u'01'))
                .timezone('UTC')
                .beginning()
            )

            end_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, month, u'01'))
                .timezone('UTC')
                .next_month()
                .beginning()
            )

        elif year and not month and day:
            from_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, u'01', day))
                .timezone('UTC')
                .beginning()
            )

            end_date = (
                Days()
                .day(u"{0}-{1}-{2}".format(year, u'12', day))
                .timezone('UTC')
                .beginning()
            )

        elif year and not month and not day:
            from_date = (
                Days().day(u"{0}-01-01".format(year))
                .timezone('UTC')
                .beginning()
            )

            end_date = (
                Days().day(u"{0}-12-31".format(year))
                .timezone('UTC')
                .beginning()
            )

        elif not year:
            self.redirect('/')

        posts = self.posts.find_posts_between_date(from_date, end_date)

        articles = []

        for article in posts:
            if 'tags' not in article:
                article['tags'] = []
            articles.append(article)

        self.render("archive.html",
                    title=u'归档 | VANELLOPE',
                    page=u'archive',
                    from_date=from_date,
                    end_date=end_date,
                    current_uri=self.request.uri,
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    articles=articles)


class CategoryPage(BaseHandler):
    def get(self, cate):
        current_page = int(self.get_argument(u'p', 1))
        articles = self.posts.find_by_category(cate)

        self.render("category.html",
                    title=u'Category:{0} | VANELLOPE'.format(cate),
                    page=u'category',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    current_category=cate,
                    articles=articles)


class LoginPage(BaseHandler):
    def get(self):
        self.render("login.html",
                    title=u'登录 | VANELLOPE',
                    page=u'login')

    def post(self):
        """Login"""

        pwd = self.get_argument('pwd', None)

        err = 0

        admin_user = self.user.get_admin_user()

        if not admin_user:
            return self.redirect('/welcome')

        new_hash = hashlib.sha256(pwd + admin_user['salt']).hexdigest()
        if admin_user['passwd'] == new_hash:
            self.clear_all_cookies()
            cookie = base64.b64encode('Admin:' + new_hash)
            self.set_cookie(name="vanellope",
                            value=cookie,
                            expires_days=90)
        else:
            err += 1

        if err == 0:
            self.redirect('/')

        else:
            self.redirect('/login')


class Logout(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


class DraftPage(BaseHandler):
    @authenticated
    def get(self, article_id):
        article = self.posts.find_by_id(article_id)

        if not article:
            self.send_error(404)
            return

        if 'tags' not in article:
            article['tags'] = []

        siblings = []

        self.render("article.html",
                    title=article['title'],
                    page=u'draft',
                    related_articles=[],
                    siblings=siblings,
                    article=article)


class ArticlePage(BaseHandler):
    def get(self, article_id):
        try:
            article = self.posts.find(id_list=[article_id],
                                      states=['published'])[0]
        except IndexError:
            self.send_error(404)
            return

        if 'tags' not in article:
            article['tags'] = []

        siblings = []

        self.render("article.html",
                    title=article['title'],
                    page=u'article',
                    related_articles=[],
                    siblings=siblings,
                    article=article)

    def post(self):
        """Create new article"""
        pass

    @authenticated
    def put(self, article_id=None):
        """ Update an existing article """
        pass

    @authenticated
    def delete(self, article_id):
        """ Delete article """
        pass


class UploadedFileHandler(web.StaticFileHandler):
    def initialize(self):
        uploaded_path = self.settings['uploaded_path']
        return web.StaticFileHandler.initialize(self, uploaded_path)
