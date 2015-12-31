# coding=utf-8

from vanellope.handlers import BaseHandler


class MainFeed(BaseHandler):
    def get(self):
        current_page = int(self.get_argument(u'p', 1))

        _posts = self.posts.get_posts()

        entries = []

        for article in _posts:
            if 'tags' not in article:
                article['tags'] = []

            article['short_path'] = '/article/' + article['uuid']
            article['long_path'] = ''.join('/article/',
                                           article['uuid'],
                                           u'_'.join(article['title'].split()))
            article['edit_path'] = '/admin/edit/' + article['long_path']
            entries.append(article)

        self.set_header('Content-Type', 'application/atom+xml; charset=UTF-8')

        self.render("feeds.xml",
                    title=u'VANELLOPE| Feeds',
                    page=u'index',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    entries=entries,
                    articles=entries)
