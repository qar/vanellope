#! /usr/bin/env python
# coding=utf-8

import datetime
from vanellope.ext import db

class Comment:
    def __init__(self, article_id):
        self.db = db.comment
        self.comment = {
            "article_id": article_id,
            "date": datetime.datetime.utcnow(),
        }

    def set_content(self, comment_content):
        self.comment['body'] = comment_content

    def set_commenter(self, commenter_object):
        self.comment['commenter'] = commenter_object


    def save(self):
        keys = ("body", "commenter" )
        if len([x for x in keys if x in self.comment.keys()]) == len(keys):
            self.db.insert(self.comment)
            return True
        else:
            return False


