# coding=utf-8

from tornado.web import authenticated
from vanellope.handlers import AdminBaseHandler
from vanellope.database import db_backup


class AdminControlPanel(AdminBaseHandler):
    @authenticated
    def get(self):
        self.render("controlpanel.html",
                    title=u"Control Panel")


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
