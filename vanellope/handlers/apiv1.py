# coding=utf-8

import os.path
import uuid
from tornado.web import authenticated
from tornado.escape import json_decode
from vanellope.handlers import BaseHandler
from vanellope import config


class ArticleHandler(BaseHandler):
    def get(self, article_id):
        article = self.posts.find_by_id(article_id)

        if not article:
            self.send_error(404)
            return

        if 'tags' not in article:
            article['tags'] = []

        article['created_at'] = article['created_at'].strftime('%s')  # seconds
        article['updated_at'] = article['updated_at'].strftime('%s')  # seconds
        self.finish(article)


class ConfigurationHandler(BaseHandler):
    @authenticated
    def get(self):
        configs = self.config.read_config()
        self.finish({
            'msg': 'success',
            'configs': configs
        })

    def put(self):
        """ 更新
        """

        configs = {}
        for k in self.settings['config_keys']:
            v = self.get_payload_argument(k, None)
            if v is not None:
                configs[k] = v

        self.config.update(configs)
        self.finish({
            'info': 'success'
        })


class ImageHandler(BaseHandler):
    @authenticated
    def post(self):
        """Upload image
        """

        ifsuccess = self.get_argument('ifsuccess', {})
        # iffail = self.get_argument('iffail', {})
        pathKey = self.get_argument('pathKey', 'url')

        image = self.request.files['image'][0]
        ext = image['filename'].split('.')[-1]

        newFilename = str(uuid.uuid4()) + '.' + ext
        fpath = os.path.join(self.settings['uploaded_path'], newFilename)
        url = '/uploaded/' + newFilename
        with open(fpath, 'wb') as f:
            f.write(image['body'])
            f.close()

        if not isinstance(ifsuccess, dict):
            ifsuccess = json_decode(ifsuccess)

        ifsuccess.update({
            pathKey: url
        })

        self.finish(ifsuccess)


class PostsHandler(BaseHandler):
    @authenticated
    def get(self):
        ENTRIES_PER_PAGE = config.posts_per_page
        current_page = int(self.get_argument(u'p', 1))

        articles = self.posts.find(
            states=['published'],
            limit=ENTRIES_PER_PAGE,
            skip=(current_page - 1) * ENTRIES_PER_PAGE
        )

        data = []
        for article in articles:
            article['created_at'] = article['created_at'].strftime('%s')
            article['updated_at'] = article['updated_at'].strftime('%s')
            data.append(article)

        self.finish({
            'info': 'success',
            'data': data
        })

    def post(self):
        """
        创建

        提交参数:
            content
            title
        """
        category = self.get_payload_argument('category', '')
        content = self.get_payload_argument('content', '')
        source = self.get_payload_argument('source', '')
        tags = self.get_payload_argument('tags', '')
        title = self.get_payload_argument('title', 'default_title')
        state = self.get_payload_argument('state', 'draft')
        ext = 'html'

        post_uuid = self.posts.create({
            'content': content,
            'source': source,
            'title': title,
            'category': category,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        url_safe_title = '_'.join(title.split())

        if state == 'draft':
            article_url = '/drafts/{0}+{1}'.format(post_uuid, url_safe_title)
        else:
            article_url = '/article/{0}+{1}'.format(post_uuid, url_safe_title)

        self.finish({
            'info': 'success',
            'url': article_url
        })

    def put(self):
        """
        更新

        提交参数:
            content
            title
        """
        category = self.get_payload_argument('category', '')
        content = self.get_payload_argument('content', '')
        post_uuid = self.get_payload_argument('uuid', '')
        tags = self.get_payload_argument('tags', '')
        title = self.get_payload_argument('title', 'default_title')
        state = self.get_payload_argument('state', 'published')
        ext = 'html'

        self.posts.update(post_uuid, {
            'uuid': post_uuid,
            'content': content,
            'title': title,
            'category': category,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        url_safe_title = '_'.join(title.split())
        if state == 'draft':
            article_url = '/drafts/{0}+{1}'.format(post_uuid, url_safe_title)
        else:
            article_url = '/article/{0}+{1}'.format(post_uuid, url_safe_title)

        self.finish({
            'info': 'success',
            'url': article_url
        })


class PostHandler(BaseHandler):
    @authenticated
    def delete(self, entry_id):
        self.posts.delete(entry_id)
        self.finish({
            'msg': 'success'
        })


class AdminTrashHandler(BaseHandler):
    @authenticated
    def delete(self, entry_id):
        self.posts.drop(entry_id)
        self.finish({
            'msg': 'success'
        })


class CommentsHandler(BaseHandler):
    def post(self):
        """
        创建

        提交参数:
            post_id
            name
            email
            website
            content
        """
        post_id = self.get_argument('post_id', '')
        name = self.get_argument('name', '')
        email = self.get_argument('email', '')
        website = self.get_argument('website', '')
        content = self.get_argument('content', '')

        self.comments.create({
            'post_id': post_id,
            'name': name,
            'email': email,
            'website': website,
            'content': content,
        })

        self.redirect(self.request.headers['Referer'])
