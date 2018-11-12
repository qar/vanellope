# coding=utf-8

from tornado.web import authenticated
from vanellope.handlers import AdminBaseHandler
from vanellope.da import db_backup


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


class FriendLinkHandler(AdminBaseHandler):
    @authenticated
    def get(self):
        friend_links = self.friendlinks.find_all()
        self.finish({
            'info': 'success',
            'data': friend_links 
        })

    @authenticated
    def put(self):
        """
        """
        site_title = self.get_payload_argument(u'site_title', None)
        site_address = self.get_payload_argument(u'site_address', None)
        site_notes = self.get_payload_argument(u'site_notes', None)
        site_uuid = self.get_payload_argument(u'site_uuid', None)

        result = self.friend_links.update(site_uuid, {
            'title': site_title,
            'address': site_address,
            'notes': site_notes,
        })

        self.finish({
            'info': 'success',
            'url': result
        })

