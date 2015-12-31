#!/usr/bin/env python
# coding: utf-8

from urlparse import urlparse
from tornado import testing
from tornado import httpclient
from vanellope import config
from vanellope import app
from tornado import ioloop

# http://www.tornadoweb.org/en/stable/testing.html#tornado.testing.AsyncHTTPTestCase

class TestPages(testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_login_page(self):
        target_url = '/login'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_logout_page(self):
        target_url = '/logout'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, '/')

    def test_index_page(self):
        target_url = '/'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_article_page(self):
        pass
        # target_url = '/article/32ea9174'
        # response = self.fetch(target_url)
        # parsed_url = urlparse(response.effective_url)
        # self.assertEqual(response.code, 200)
        # self.assertEqual(parsed_url.path, target_url)

    def test_tags_page(self):
        target_url = '/tags'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_tag_page(self):
        target_url = '/tags/vanellope'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_archives_page(self):
        target_url = '/archives'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_category_page(self):
        target_url = '/category/vanellope'
        response = self.fetch(target_url)
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 200)
        self.assertEqual(parsed_url.path, target_url)

    def test_archive_page(self):
        pass


    def test_admin_page(self):
        # http://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.HTTPResponse

        target_url = '/admin'
        response = self.fetch(target_url,
            follow_redirects = False
        )
        parsed_url = urlparse(response.effective_url)
        self.assertEqual(response.code, 302)
        self.assertEqual(parsed_url.path, target_url)


if __name__ == '__main__':
    unittest.main()
