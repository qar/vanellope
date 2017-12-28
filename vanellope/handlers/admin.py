# coding=utf-8

from tornado.web import authenticated
from vanellope.handlers import AdminBaseHandler
from vanellope.database import db_backup


class AdminSettingsPage(AdminBaseHandler):
    @authenticated
    def get(self):
        self.render("admin.html",
                    title=self.concat_page_title('Admin'),
                    page=u'admin/settings')


class AdminEditPage(AdminBaseHandler):
    @authenticated
    def get(self, article_id=None):
        article = self.posts.find_by_id(article_id)

        if article_id and article is None:
            return self.send_error(404)

        self.render("write.html",
                    title=self.concat_page_title('Editing'),
                    page=u'admin/edit',
                    article=article)


class AdminDraftsPage(AdminBaseHandler):
    @authenticated
    def get(self):
        articles = self.posts.get_drafts()

        self.render("drafts.html",
                    title=self.concat_page_title('Drafts'),
                    page=u'admin/drafts',
                    articles=articles)


class AdminControlPanel(AdminBaseHandler):
    @authenticated
    def get(self):
        self.render("controlpanel.html")


class AdminTrashPage(AdminBaseHandler):
    @authenticated
    def get(self):
        articles = self.posts.get_trash()

        self.render("trash.html",
                    title=self.concat_page_title('Trash'),
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
