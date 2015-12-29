#!/usr/bin/env python
# coding: utf-8

from tornado.testing import unittest
from tornado import gen
from vanellope import database

class TestDatabasePostModel(unittest.TestCase):
    def setUp(self):
        self.posts = database.PostModel()

    def test_get_posts(self):
        posts = self.posts.get_posts()
        self.assertIs(type(posts), list)

    def test_create(self):
        sample = None
        self.assertRaises(TypeError, self.posts.create, sample)

        sample = {}
        self.assertRaises(KeyError, self.posts.create, sample)

        sample = {
            'ext': 'html',
            'title': '1234',
            'content': '1234'
        }



if __name__ == '__main__':
    unittest.main()
