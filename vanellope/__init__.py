#! /usr/bin/env python
# coding=utf-8

import pymongo
import requests
import config

db = pymongo.Connection(config.DB_HOST, config.DB_PORT)['page302']


class Mail:
	def __init__(self, Subject=None, To=None, Body=None):
		self.url = config.MAIL_API_URL
		self.auth = config.MAIL_API_AUTH
		self.mail_from = config.MAIL_FROM
		self.mail_to = To
		self.subject = Subject
		self.body = Body

	def Subject(self, _subject):
		self.subject = _subject

	def From(self, _from):
		self.mail_from = _from

	def To(self, _to):
		self.mail_to = _to

	def Body(self, _body):
		self.body = _body

	def Send(self):
		return requests.post(
			self.url,
			auth = self.auth,
			data = {"from":self.mail_from,
					"to": [self.mail_to,],
					"subject": self.subject,
					"html": self.body})



def filter(text):
	# Convert raw @somone to <a href="/SomeURLAboutsomeone"></a>
	patt = ""