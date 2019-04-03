# coding=utf-8

import config

from vanellope.handlers import pages
from vanellope.handlers import apiv1
from vanellope.handlers import admin
from vanellope.handlers import feeds

routers = [
    (r"/welcome", pages.WelcomePage),

    # Index page
    (r"/", pages.IndexPage),

    (r"/tags", pages.TagsPage),
    (r"/archives", pages.ArchivesPage),

    # Articles about one specific tag
    (r"/tags/(.*)", pages.TagPage),

    # Show articles written in a specific date range
    # accept date range from 0000-00-00 to 9999-99-99
    (r"/archive/([0-9]{4})?/?([0-9]{2})?/?([0-9]{2})?", pages.ArchivePage),

    # Articles with one specific category
    (r"/category/(.*)", pages.CategoryPage),

    # GET 查看某篇文章
    (r"/article/(\w{8}).*", pages.ArticlePage),

    # Notes
    (r"/notes", pages.NotesPage),

    # 查看草稿
    (config.app_settings['draft_base_path'] + r"(\w{8}).*", pages.DraftPage),

    # 登出
    (r"/logout", pages.Logout),
    (r"/login", pages.LoginPage),

    (r"/uploaded/(.*)", pages.UploadedFileHandler),

    (r"/api/v1/access-tokens", apiv1.AccessTokensHandler),
    (r"/api/v1/access-tokens/(.*)", apiv1.AccessTokensHandler),
    (r"/api/v1/tags", apiv1.TagsHandler),
    (r"/api/v1/trash", apiv1.TrashHandler),
    (r"/api/v1/notes", apiv1.NotesHandler),
    (r"/api/v1/notes/(.*)", apiv1.NotesHandler),
    (r"/api/v1/posts", apiv1.PostsHandler),
    (r"/api/v1/article/(.*)", apiv1.PostHandler), # deprecated
    (r"/api/v1/posts/(.*)", apiv1.PostHandler),
    (r"/api/v1/image", apiv1.ImageHandler),
    (r"/api/v1/configuration", apiv1.ConfigurationHandler),
    (r"/api/v1/admin/trash/(.*)", apiv1.AdminTrashHandler),
    (r"/api/v1/comments", apiv1.CommentsHandler),
    (r"/api/v1/categories", apiv1.CategoryListHandler),
    (r"/api/v1/admin/friend-links", admin.FriendLinkHandler),
    (r"/api/v1/admin/friend-links/(.*)", admin.FriendLinkHandler),

    # Feeds
    (r"/index.xml", feeds.MainFeed),

    # Administrotor URLs
    (r"/admin/export", admin.AdminExportData),
    (r"/controlpanel", admin.AdminControlPanel)
]
