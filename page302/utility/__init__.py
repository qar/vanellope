# coding=utf-8
import urllib
import hashlib

def simple_content_parser():
	# simple plain text parser:
	# '#sometext' --> <h1>sometext</h1>
	# 
	pass

def Avatar(email):
	# Using Gravatar
	default = "static/img/avatar/default.png"
	size = 128
	gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
					hashlib.md5(email.lower()).hexdigest() + "?")
	gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
	return gravatar_url



