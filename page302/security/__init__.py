#! /usr/bin/env python
# coding=utf-8
import os
import sys
import os.path
import pymongo

import settings
import tornado.web
        

def CheckAuth(auth_cookie):
    # take a cookie name that do authentication function
    db_member = settings.DATABASE['member']
    member = db_member.find_one({"auth": auth_cookie})
    print type(member)
    if member:
        return member
    else:
        return None


    





