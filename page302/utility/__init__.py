# coding=utf-8
import urllib
import hashlib

def simple_content_parser():
	# simple plain text parser:
	# '#sometext' --> <h1>sometext</h1>
	# 
	pass

def Avatar(email, size=128, ):
	# Using Gravatar
	LARGE = 128
	gravatar_url = ("http://www.gravatar.com/avatar/%s" % 
					hashlib.md5(email.lower()).hexdigest() + "?")
	# use local default avatar
	#gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
	#default = "static/img/avatar/default.png"

	# use gravatar default img
	gravatar_url += urllib.urlencode({'s':str(size)})
	return gravatar_url



