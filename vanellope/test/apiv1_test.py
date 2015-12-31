#!/usr/bin/env python
# coding: utf-8

from urlparse import urlparse
from tornado import testing
from tornado import httpclient
from vanellope import config
from vanellope import app
from tornado import ioloop
import json

# http://www.tornadoweb.org/en/stable/testing.html#tornado.testing.AsyncHTTPTestCase

class TestApiv1(testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get_api_v1_article_name(self):
        pass
        # target_url = '/api/v1/article/32ea9174'
        # response = self.fetch(target_url)
        # parsed_url = urlparse(response.effective_url)
        # self.assertEqual(response.code, 200)
        # self.assertEqual(parsed_url.path, target_url)
        # body = json.loads(response.body)

        # expected_keys = [
        #     u'category',
        #     u'ext',
        #     u'uuid',
        #     u'title',
        #     u'created_at',
        #     u'tags',
        #     u'updated_at',
        #     u'content',
        #     u'state'
        # ]

        # self.assertSequenceEqual(body.keys(), expected_keys);
        # self.assertTrue(isinstance(body['category'], unicode));
        # self.assertTrue(isinstance(body['state'], unicode));
        # self.assertTrue(isinstance(body['uuid'], unicode));
        # self.assertTrue(isinstance(body['created_at'], unicode));
        # self.assertTrue(isinstance(body['tags'], list));
        # self.assertTrue(isinstance(body['content'], unicode));
        # self.assertTrue(isinstance(body['ext'], unicode));


if __name__ == '__main__':
    unittest.main()
