# coding=utf-8

import config
from tornado import web

from vanellope.handlers import pages
from vanellope.handlers import apiv1
from vanellope.handlers import admin
from vanellope.handlers import feeds

routers = [
    (r"/welcome", pages.WelcomePage),

    # Index page
    (r"/", pages.IndexPage),

    # 登录
    (r"/authentication", pages.WelcomePage),

    (r"/tags", pages.TagsPage),
    (r"/archives", pages.ArchivesPage),

    # Articles about one specific tag
    (r"/tags/(.*)", pages.TagPage),

    # Show articles written in a specific date range
    # accept date range from 0000-00-00 to 9999-99-99
    (r"/archive/([0-9]{4})/?([0-9]{2})?/?([0-9]{2})?", pages.ArchivePage),

    # Articles with one specific category
    (r"/category/(.*)", pages.CategoryPage),

    # GET 查看某篇文章
    (r"/article/(\w{8}).*", pages.ArticlePage),

    # 查看草稿
    (config.app_settings['draft_base_path'] + r"(\w{8}).*", pages.DraftPage),

    # 登出
    (r"/logout", pages.Logout),
    (r"/login", pages.LoginPage),

    (r"/uploaded/(.*)", pages.UploadedFileHandler),

    (r"/api/v1/posts", apiv1.PostsHandler),
    (r"/api/v1/posts/(.*)", apiv1.PostHandler),
    (r"/api/v1/article/(.*)", apiv1.ArticleHandler),
    (r"/api/v1/image", apiv1.ImageHandler),
    (r"/api/v1/configuration", apiv1.ConfigurationHandler),
    (r"/api/v1/admin/trash/(.*)", apiv1.AdminTrashHandler),

    # Feeds
    (r"/index.xml", feeds.MainFeed),

    # Administrotor URLs
    (r"/admin", admin.AdminSettingsPage),
    (r"/admin/drafts", admin.AdminDraftsPage),
    (r"/admin/trash", admin.AdminTrashPage),
    (r"/admin/settings", admin.AdminSettingsPage),
    (r"/admin/edit", admin.AdminEditPage),
    (r"/admin/edit/(\w{8})\+.*", admin.AdminEditPage),
    (r"/admin/export", admin.AdminExportData)
]
