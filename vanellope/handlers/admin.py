# coding=utf-8

from tornado.web import authenticated
from vanellope.handlers import AdminBaseHandler
from vanellope.database import db_backup


class AdminSettingsPage(AdminBaseHandler):
    @authenticated
    def get(self):
        self.render("admin.html",
                    title=u'VANELLOPE| Admin',
                    page=u'admin/settings')


class AdminEditPage(AdminBaseHandler):
    @authenticated
    def get(self, article_id=None):
        article = self.posts.find_by_id(article_id)

        if article_id and article is None:
            return self.send_error(404)

        self.render("write.html",
                    title=u'VANELLOPE| Editing',
                    page=u'admin/edit',
                    article=article)


class AdminDraftsPage(AdminBaseHandler):
    @authenticated
    def get(self):
        articles = self.posts.get_drafts()

        self.render("drafts.html",
                    title=u'VANELLOPE| Drafts',
                    page=u'admin/drafts',
                    articles=articles)


class AdminTrashPage(AdminBaseHandler):
    @authenticated
    def get(self):
        articles = self.posts.get_trash()

        self.render("trash.html",
                    title=u'VANELLOPE| Trash',
                    page=u'admin/trash',
                    articles=articles)


class AdminExportData(AdminBaseHandler):
    def get(self):
        """Export database
        """
        zip_path, zip_filename = db_backup()

        with open(zip_path, 'rb') as f:
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition',
                            'attachment; filename=' + zip_filename)
            self.write(f.read())
            self.finish()
