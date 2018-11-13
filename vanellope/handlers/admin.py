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

        data = []
        for link in friend_links:
            link['created_at'] = link['created_at'].strftime('%s')
            link['updated_at'] = link['updated_at'].strftime('%s')
            data.append(link)

        self.finish({
            'info': 'success',
            'data': data
        })

    @authenticated
    def post(self):
        """
        """
        site_title = self.get_payload_argument(u'title', None)
        site_address = self.get_payload_argument(u'address', None)
        site_notes = self.get_payload_argument(u'notes', None)

        result = self.friendlinks.create({
            'title': site_title,
            'address': site_address,
            'notes': site_notes
        })

        self.finish({
            'info': 'success',
            'url': result
        })

    @authenticated
    def delete(self, uuid):
        result = self.friendlinks.remove(uuid)

        self.finish({
            'info': 'success',
            'url': result
        })


