# coding=utf-8

import os.path
import uuid
from tornado.web import authenticated
from tornado.escape import json_decode
from vanellope.handlers import BaseHandler


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
    def get(self):
        self.finish()

    def post(self):
        """
        创建

        提交参数:
            content
            title
        """
        category = self.get_payload_argument('category', '')
        content = self.get_payload_argument('content', '')
        tags = self.get_payload_argument('tags', '')
        title = self.get_payload_argument('title', 'default_title')
        state = self.get_payload_argument('state', 'draft')
        ext = 'html'

        post_uuid = self.posts.create({
            'content': content,
            'title': title,
            'category': category,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        if state == 'draft':
            article_url = '/drafts/' + post_uuid + '+' + "_".join(title.split())
        else:
            article_url = '/article/' + post_uuid + '+' + "_".join(title.split())

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
        uuid = self.get_payload_argument('uuid', '')
        tags = self.get_payload_argument('tags', '')
        title = self.get_payload_argument('title', 'default_title')
        state = self.get_payload_argument('state', 'published')
        ext = 'html'

        self.posts.update(uuid, {
            'uuid': uuid,
            'content': content,
            'title': title,
            'category': category,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        if state == 'draft':
            article_url = '/drafts/' + post_uuid + '+' + "_".join(title.split())
        else:
            article_url = '/article/' + post_uuid + '+' + "_".join(title.split())

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
