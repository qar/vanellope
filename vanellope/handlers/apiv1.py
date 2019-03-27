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

        result = self.config.update(configs)
        self.finish({
            'info': 'success',
            'data': result
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
        ENTRIES_PER_PAGE = 10
        # config.posts_per_page
        current_page = int(self.get_argument(u'p', 1))
        items_per_page = int(self.get_argument(u'z', ENTRIES_PER_PAGE))
        states = self.get_arguments(u's[]')

        articles = self.posts.find(
            states=states,
            limit=items_per_page,
            skip=(current_page - 1) * items_per_page
        )

        total_items = self.posts.count(states=states)

        data = []
        for article in articles:
            article['created_at'] = article['created_at'].strftime('%s')
            article['updated_at'] = article['updated_at'].strftime('%s')
            data.append(article)

        self.finish({
            'info': 'success',
            'paging': {
                'total': total_items,
                'items_per_page': items_per_page,
                'current_page': current_page,
            },
            'data': data
        })

    @authenticated
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
        summary = self.get_payload_argument('summary', '')
        ext = self.get_payload_argument('ext', 'markdown')

        post_uuid = self.posts.create({
            'content': content,
            'source': source,
            'summary': summary,
            'title': title,
            'category': category,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        url_safe_title = '_'.join(title.split())

        if state == u'draft':
            article_url = u'/drafts/{0}+{1}'.format(post_uuid, url_safe_title)
        else:
            article_url = u'/article/{0}+{1}'.format(post_uuid, url_safe_title)

        self.finish({
            'info': 'success',
            'url': article_url
        })


class TrashHandler(BaseHandler):
    @authenticated
    def get(self):
        ENTRIES_PER_PAGE = 10
        # config.posts_per_page
        current_page = int(self.get_argument(u'p', 1))
        items_per_page = int(self.get_argument(u'z', ENTRIES_PER_PAGE))

        articles = self.posts.find(
            states=['deleted'],
            limit=items_per_page,
            skip=(current_page - 1) * items_per_page
        )

        total_items = self.posts.count(states=['deleted'])

        data = []
        for article in articles:
            article['created_at'] = article['created_at'].strftime('%s')
            article['updated_at'] = article['updated_at'].strftime('%s')
            data.append(article)

        self.finish({
            'info': 'success',
            'paging': {
                'total': total_items + 0,
                'items_per_page': items_per_page,
                'current_page': current_page,
            },
            'data': {
                'articles': data,
                'snippets': []
            }
        })


class PostHandler(BaseHandler):
    @authenticated
    def delete(self, entry_id):
        self.posts.delete(entry_id)
        self.finish({
            'msg': 'success'
        })

    @authenticated
    def put(self, post_uuid):
        """
        更新

        提交参数:
            content
            title
        """
        category = self.get_payload_argument('category', '')
        content = self.get_payload_argument('content', '')
        source = self.get_payload_argument('source', '')
        tags = self.get_payload_argument('tags', '')
        title = self.get_payload_argument('title', 'default_title')
        state = self.get_payload_argument('state', 'published')
        summary = self.get_payload_argument('summary', '')
        ext = self.get_payload_argument('ext', 'markdown')

        self.posts.update(post_uuid, {
            'uuid': post_uuid,
            'source': source,
            'content': content,
            'title': title,
            'category': category,
            'summary': summary,
            'tags': tags,
            'ext': ext,
            'state': state
        })

        url_safe_title = '_'.join(title.split())
        if state == 'draft':
            article_url = u'/drafts/{0}+{1}'.format(post_uuid, url_safe_title)
        else:
            article_url = u'/article/{0}+{1}'.format(post_uuid, url_safe_title)

        self.finish({
            'info': 'success',
            'url': article_url
        })


class AdminTrashHandler(BaseHandler):
    @authenticated
    def delete(self, entry_id):
        self.posts.drop(entry_id)
        self.finish({
            'msg': 'success'
        })


class CommentsHandler(BaseHandler):
    @authenticated
    def get(self):
        ENTRIES_PER_PAGE = 10
        # config.posts_per_page
        current_page = int(self.get_argument(u'p', 1))
        items_per_page = int(self.get_argument(u'z', ENTRIES_PER_PAGE))
        states = self.get_arguments(u's[]')

        comments = self.comments.find(
            states=states,
            limit=items_per_page,
            skip=(current_page - 1) * items_per_page
        )

        total_items = self.comments.count(states=states)

        data = []
        for c in comments:
            c['created_at'] = c['created_at'].strftime('%s')
            data.append(c)

        self.finish({
            'info': 'success',
            'paging': {
                'total': total_items,
                'items_per_page': items_per_page,
                'current_page': current_page,
            },
            'data': data
        })

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
            'role': self.current_user['role']
        })

        self.redirect(self.request.headers['Referer'])

    @authenticated
    def put(self):
        """Update comment

        Authentication requred.
        This handler may be used to update comment check status.
        """
        try:
            comment_id = self.get_payload_argument('uuid', None)
            state = self.get_payload_argument('state', None)

            if not comment_id:
                raise Exception('required argument missing: uuid')

            if not state:
                raise Exception('required argument missing: state')

            self.comments.update(comment_id, {
                'state': state
            })

            self.finish({
                'info': 'success'
            })

        except Exception, e:
            self.set_status(400)
            self.finish({ 'reason': str(e) })


class CategoryListHandler(BaseHandler):
    @authenticated
    def get(self):
        """
        Find all categories
        """
        categories = self.posts.get_categories()
        self.finish({
            'info': 'success',
            'data': categories
            })


class NotesHandler(BaseHandler):
    @authenticated
    def post(self):
        content = self.get_payload_argument('content', '')

        note_uuid = self.notes.create({
            'content': content
            })

        self.finish({
            'info': 'success'
            })
