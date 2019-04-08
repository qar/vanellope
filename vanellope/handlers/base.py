# coding=utf-8

import urllib
import string
import random
import hashlib
import uuid
import re
import os
import pytz

import itertools
from datetime import datetime, timedelta
from dateutil import relativedelta

import base64
from tornado.web import RequestHandler, MissingArgumentError
from tornado.log import access_log
from tornado.escape import json_decode

from user_agents import parse as ua_parse
import urlparse

from vanellope.handlers.static import MyStaticFileHandler

from vanellope.da.config import ConfigModel
from vanellope.da.user import UserModel
from vanellope.da.post import PostModel
from vanellope.da.notes import NoteModel
from vanellope.da.accesstoken import AccessTokenModel
from vanellope.da.session import Session
from vanellope.da.comment import CommentModel
from vanellope.da.friendlinks import FriendLinkModel


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
    notes = NoteModel()
    config = ConfigModel()
    session = Session()
    comments = CommentModel()
    friendlinks = FriendLinkModel()
    accessToken = AccessTokenModel()

    def base_uri(self):
        """Get request.uri but Remove query string

        e.q. `/path/to/path?p=1` to `/path/to/path`
        """
        return self.request.uri.rsplit('?', 1)[0]

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

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

        session_id = self.get_cookie('s')

        if not session_id:
            session_id = str(uuid.uuid4())
            # Set session
            self.set_cookie(name="s", value=session_id)

        self.current_user = self.get_current_user()

        if not self.current_user:
            self.session.record_visitor(session_id, 'Anonymous', self.request.remote_ip, user_agent)
            session_check = self.session.check_visitor(session_id)

            if session_check['requests'] > 5:
                self.set_status(403)
                self.finish('Access Denied')
                return

        # if the site is just created without a admin user
        if not self.settings['admin']:
            if self.request.uri.startswith('/api'):
                self.set_status(403)
                self.finish('login first')

            elif self.request.uri != '/welcome':
                self.redirect('/welcome')

    def get_template_namespace(self):
        """Override `tornado.web.RequestHandler.get_template_namespace` static method
        add those new features:

        """

        namespace = super(BaseHandler, self).get_template_namespace()
        namespace.update({
            'site': self.config.read_config(),
            'ctx': {
                'year': datetime.now().year
            }
        })

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
        namespace['categories'] = self.posts.get_categories()
        namespace['friendlinks'] = self.friendlinks.find_all()

        return namespace

    def get_payload_argument(self, name, default, strip=True):
        """ Get request data from payload

        """
        source = json_decode(self.request.body)
        if not isinstance(source, dict):
            raise MissingArgumentError(name)

        if name not in source:
            return default

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
        try:
            auth = self.get_cookie('vanellope')
            username, passwd_hash = base64.b64decode(auth).split(':')
            user = self.user.get_user_by_name(username)
            if user['passwd'] == passwd_hash:
                return user
            else:
                return
        except Exception, e:
            return

    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def concat_page_title(self, page_title):
        site_title = self.get_template_namespace()['site']['site_title']
        return site_title + '| ' + page_title

    def get_themes(self):
        buildin = os.listdir(self.settings['themes_dir'])
        custom = os.listdir(self.settings['custom_themes_dir'])
        return buildin + custom;

    def change_theme(self, theme):
        buildin_themes_dir = self.settings['themes_dir']
        custom_themes_dir = self.settings['custom_themes_dir']

        buildin = os.listdir(buildin_themes_dir)
        root_path = buildin_themes_dir if theme in buildin else custom_themes_dir

        self.config.set_value('site_theme', theme)
        self.settings['theme'] = theme
        self.settings['theme_config_path'] = os.path.join(root_path, "%s/config.yaml" % theme)
        self.settings['static_path'] = os.path.join(root_path, "%s/static" % theme)
        self.settings['template_path'] = os.path.join(root_path, "%s/templates" % theme)
        MyStaticFileHandler.reset()


class AdminBaseHandler(BaseHandler):
    def static_url(self, path, include_host=None, **kwargs):
        """Override original static_url method to server admin static files
        """
        self.require_setting("admin_static_path", "static_url")
        get_url = self.settings.get("static_handler_class",
                                    MyStaticFileHandler).make_static_url

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

    def concat_page_title(self, page_title):
        site_title = self.get_template_namespace()['site']['site_title']
        return site_title + '| ' + page_title
