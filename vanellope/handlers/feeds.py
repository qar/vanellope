# coding=utf-8

import math
from vanellope.handlers.base import BaseHandler


class MainFeed(BaseHandler):
    def get(self):
        site_config = self.config.read_config()
        ENTRIES_PER_PAGE = site_config['posts_per_page']
        current_page = int(self.get_argument(u'p', 1))

        _posts  = self.posts.find(
            states=['published'],
            limit=ENTRIES_PER_PAGE,
            skip=(current_page - 1) * int(ENTRIES_PER_PAGE)
        )

        total_entries = self.posts.count(states=['published'])

        pages = int(math.ceil(total_entries / float(ENTRIES_PER_PAGE)))

        # 1 page bigger than currnet page, but not bigger than total pages
        next_page = current_page + 1 if current_page < pages else pages

        # 1 page less than currnet page, but at least page 1
        previous_page = current_page - 1 if current_page > 1 else 1

        self.set_header('Content-Type', 'application/atom+xml; charset=UTF-8')

        self.render("feeds.xml",
                    title=self.concat_page_title('Feeds'),
                    page=u'index',
                    previous_page=current_page - 1 if current_page > 1 else 1,
                    next_page=current_page + 1,
                    entries=_posts)
