from vanellope.handlers.base import BaseHandler

class Error404Handler(BaseHandler):
    def get(self):
        ns = self.get_template_namespace()

        self.render("404.html",
                    title=self.concat_page_title('Welcome'),
                    description=ns['site']['site_description'],
                    page=u'welcome')
