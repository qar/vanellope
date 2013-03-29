#! /usr/bin/env python
# coding=utf-8

import sys
import os
from test.member import member_test
from vanellope import db
from vanellope.model import Member

if __name__ == "__main__":
	sys.path.append(os.getcwd())
	c = db.member.find_one()
	member = Member(entity=c)
	print dir(member)
	print member['auth']
	try:
		print member['_id']
	except KeyError:
		print "no such key"
