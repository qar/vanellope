#! /usr/bin/env python
# coding=utf-8

from vanellope.handlers import ajax, auth, member, article, comment, index

handlers = []
handlers.extend(ajax.handlers)
handlers.extend(member.handlers)
handlers.extend(article.handlers)
handlers.extend(comment.handlers)
handlers.extend(index.handlers)
handlers.extend(auth.handlers)
