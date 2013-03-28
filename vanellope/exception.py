#! /usr/bin/env python
# coding=utf-8

class DupKeyError(Exception):
	# This exception is raised when user want to put a new document
	#  which's key is exist
	pass

class PatternMatchError(Exception):
	# This exception is raised when regex pattern not match
	pass

class AuthError(Exception):
	# Raised when login name and pwd doesn't match Database stored value
	pass

class NameError(Exception):
	pass
	