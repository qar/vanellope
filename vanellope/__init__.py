#! /usr/bin/env python
# coding=utf-8

import re
import urllib
import hashlib
import datetime

from vanellope.ext import db

from urllib import quote_plus as url_escape

class Member:
	# Required Properties
	uid = None
	role = None
	name = None
	name_safe = None
	email = None
	pwd = None 
	auth = None
	date = None
	avatar = None
	brief = None
	verified = False


class Article:
	# Required Properties
	sn = None
	status = None
	avatar = None
	author = None
	heat = None
	title = None 
	brief = None
	body = None
	date = None
	review = None
	permalink = None
	category = None






