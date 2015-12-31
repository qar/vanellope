# coding=utf-8

import urllib
import string
import random
import hashlib
import re
import pytz

import itertools
from datetime import datetime, timedelta
from dateutil import relativedelta

import base64
from tornado.web import StaticFileHandler, RequestHandler, MissingArgumentError
from tornado.log import access_log
from tornado.escape import json_decode

from user_agents import parse as ua_parse
import urlparse

from vanellope.database import ConfigModel
from vanellope.database import UserModel
from vanellope.database import PostModel
from vanellope.database import Session


class Days(object):
    TIMEZONES = list(itertools.chain(*pytz.country_timezones.values()))
    timezone = None

    def day(self, day, tz="UTC"):
        """ when we accept the day string, we assume it's in local timezone"""
        # if the 'day' parameter is not specified, return today's beginning
        if (day and isinstance(day, basestring) and
           re.match('^\d{4}-\d{2}-\d{2}$', day)):

            self.day = datetime.strptime(day, '%Y-%m-%d')
        else:
            x = datetime.today().replace(tzinfo=pytz.timezone(tz))
            day = (x + x.utcoffset()).strftime('%Y-%m-%d')
            self.day = datetime.strptime(day, '%Y-%m-%d')

        return self

    def timezone(self, tz):
        # tz parameter maybe invalid
        if tz is not None and tz not in self.TIMEZONES and tz != 'UTC':
            self.timezone = ""
        else:
            self.timezone = tz

        return self

    def beginning(self):
        return self.day.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=pytz.timezone(self.timezone)
        )

    def next_day(self):
        self_fake = self
        self_fake.day = self.day + timedelta(days=1)
        return self_fake

    def next_month(self):
        self_fake = self
        self_fake.day = self.day + relativedelta.relativedelta(months=1)
        return self_fake

    def next_year(self):
        self_fake = self
        self_fake.day = self.day + relativedelta.relativedelta(years=1)
        return self_fake


class BaseHandler(RequestHandler):
    user = UserModel()
    posts = PostModel()
    config = ConfigModel()
    session = Session()

    def prepare(self):
        try:
            user_agent = self.request.headers['User-Agent']
        except KeyError:
            user_agent = '-'

        access_log.info('request log -> %s|%s|%s|%s' % (
            self.request.remote_ip,
            self.request.method,
            self.request.uri,
            user_agent)
        )

        if not self.settings['admin'] and self.request.method == 'GET' and self.request.uri != '/welcome':
            self.redirect('/welcome')

    def get_template_namespace(self):
        """Override `tornado.web.RequestHandler.get_template_namespace` static method
        add those new features:

        """

        namespace = super(BaseHandler, self).get_template_namespace()
        namespace['site'] = self.config.read_config()

        try:
            user_agent = self.request.headers['User-Agent']
        except KeyError:
            user_agent = '-'

        namespace['req'] = {

            # 当前请求路径
            'path': urlparse.urlparse(self.request.uri).path,

            'hostname': self.request.protocol + '://' + self.request.host,

            # userAgent 实例
            'user_agent': ua_parse(user_agent)
        }

        namespace['archives'] = self.posts.get_archives()
        namespace['tags'] = self.posts.get_tags()
        namespace['categories'] = []

        return namespace

    def get_payload_argument(self, name, default, strip=True):
        """ Get request data from payload

        """
        source = json_decode(self.request.body)
        if isinstance(source, dict):
            if name in source:
                arg = source[name]
                if isinstance(arg, basestring):
                    arg = self.decode_argument(arg)
                    # Get rid of any weird control chars (unless decoding gave
                    # us bytes, in which case leave it alone)
                    arg = RequestHandler._remove_control_chars_regex.sub(" ", arg)
                    if strip:
                         arg = arg.strip()

                elif isinstance(arg, list):
                    arg = filter(lambda item: self.decode_argument(item).strip(), arg)
                return arg
            else:
                return default

        raise MissingArgumentError(name)

    def gravatar(self, email, size=64):
        gravatar_url = ("http://www.gravatar.com/avatar/%s" %
                        hashlib.md5(email).hexdigest() + "?")
        gravatar_url += urllib.urlencode({'s': str(size)})
        return gravatar_url

    def randomwords(self, length):
        random.seed()
        chars = string.lowercase + string.uppercase + string.digits
        return ''.join(random.choice(chars) for i in range(length))

    def get_hash_string(self, origin_string):
        return hashlib.sha256(origin_string).hexdigest()

    def is_number(self, arg):
        return isinstance(arg, int)

    def get_current_user(self):
        auth = self.get_cookie('vanellope')
        if not auth:
            return

        try:
            username, passwd_hash = base64.b64decode(auth).split(':')
        except:
            return None

        if not username:
            return None
        else:
            user = self.user.get_admin_user()
            return user

    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)


class AdminBaseHandler(BaseHandler):
    def static_url(self, path, include_host=None, **kwargs):
        """Override original static_url method to server admin static files
        """
        self.require_setting("admin_static_path", "static_url")
        get_url = self.settings.get("static_handler_class",
                                    StaticFileHandler).make_static_url

        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""

        settings = dict(
            static_url_prefix=self.settings['admin_static_url_prefix'],
            static_path=self.settings['admin_static_path']
        )
        return base + get_url(settings, path, **kwargs)

    def get_template_path(self):
        """Overide default self.get_template_path method.

        In order to render admin page independently
        """
        return self.application.settings.get("admin_template_path")
