#! /usr/bin/env python
# coding=utf-8

import settings

class Member:
    def __init__(self, db=settings.DATABASE.member):
        self.db = db
        self.template = {
            "_id": None,
            "role": 1,
            "name": None,
            "name_low": None,
            "email": None,
            "pwd": None,
            "auth": None,
            "date": None,
            "avatar": None,
        }
    

