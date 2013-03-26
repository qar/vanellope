#! /usr/bin/env python
# coding=utf-8
# "da" means Data Access, this file contains various quick (or dirty) methods for accessing data.
#
#
from vanellope.ext import db

def get_member_by_name(_name):
    return db.member.find_one({"name": _name})

# this maybe dangerous, should reconsider it.
def get_member_by(**kwarg):
    return db.member.find_one(**kwarg)

def get_member_by_email_lower(_email):
    return db.member.find_one({"email": _email.lower()})

def total_member():
    return db.member.count()

def insert_new_member(_entry):
    db.member.insert(_entry)

def save_member(_entry):
    db.member.save(_entry)






