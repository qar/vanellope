#! /usr/bin/env python
# coding=utf-8
# "da" means Data Access, this file contains various quick (or dirty) methods for accessing data.
#
#
from vanellope.model import Member
from vanellope import db

def get_member_by_name(_name):
    entity = db.member.find_one({"name": _name})
    if entity:
    	return Member(entity=entity)
    else:
    	return None

# this maybe dangerous, should reconsider it.
def get_member_by_secret_key(key):
    return db.member.find_one({"secret_key":key})

def get_member_by_email_lower(_email):
    return db.member.find_one({"email": _email.lower()})

def total_member():
    return db.member.count()

def insert_new_member(_entry):
    db.member.insert(_entry)

def save_member(_entry):
    db.member.save(_entry)






