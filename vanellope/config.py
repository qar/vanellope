#! /usr/bin/env python
# coding=utf-8

"""
Default configurations.
Those can be overide by user specify settings
"""

import os
import os.path

content_path = os.environ['VANELLOPE_CONTENT']

# The theme name
theme = 'default'

# How many post displayed on one page
posts_per_page = 10

# SQLite3 Settings
db_path = os.path.join(content_path, u'data.db')

if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# 数据库备份目录
backup_path = os.path.join(content_path, u'backups/')
if not os.path.exists(os.path.dirname(backup_path)):
    os.makedirs(os.path.dirname(backup_path))

# 上传文件的存储路径
# 绝对路径
uploaded_path = os.path.join(content_path, u'www/')

if not os.path.exists(os.path.dirname(uploaded_path)):
    os.makedirs(os.path.dirname(uploaded_path))

create_table_sqls = [
    """
    CREATE TABLE IF NOT EXISTS posts (
         uuid TEXT PRIMARY KEY,
         ext TEXT,
         title TEXT,
         source TEXT,
         content TEXT,
         category TEXT NOT NULL,
         tags TEXT,
         state TEXT NOT NULL DEFAULT 'published',
         created_at TIMESTAMP NOT NULL,
         updated_at TIMESTAMP NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS views (
         post_id TEXT PRIMARY KEY,
         counts INT,
         created_at TIMESTAMP NOT NULL,
         updated_at TIMESTAMP NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        email_verified TEXT DEFAULT 'no',
        secret_key TEXT,
        passwd TEXT,
        salt TEXT,
        role TEXT,
        created_at NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS configuration (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS comments (
         uuid TEXT PRIMARY KEY,
         post_id TEXT,
         name TEXT,
         email TEXT NOT NULL,
         website TEXT,
         content TEXT NOT NULL,
         state TEXT NOT NULL DEFAULT 'checking',
         created_at TIMESTAMP NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS friendlinks (
         uuid TEXT PRIMARY KEY,
         title TEXT,
         address TEXT NOT NULL,
         notes TEXT,
         created_at TIMESTAMP NOT NULL,
         updated_at TIMESTAMP NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS notes (
         uuid TEXT PRIMARY KEY,
         content TEXT,
         created_at TIMESTAMP NOT NULL,
         updated_at TIMESTAMP NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS tokens (
         token TEXT PRIMARY KEY,
         note TEXT,
         created_at TIMESTAMP NOT NULL
    )
    """
]

app_settings = {
    # 网站标题
    'site_title': 'Life with vanellope',
    'site_description': 'Life with vanellope',
    'site_lang': 'zh-CN',

    # 网站地址 like 「www.example.com」
    'site_url': '',

    'site_theme': 'default',

    # 网站统计服务
    'site_tracking': '',  # 'google_analystics'
    'site_tracking_id': '',
    'site_tracking_enabled': 'yes',

    # Google AdSense
    'google_adsense': '',

    'ads_txt': '',

    # 网站评论服务
    'site_comment': '',  # 'duoshuo' or 'disqus'
    'site_comment_id': '',
    'site_comment_enabled': 'no',

    # Post default category
    # 新建文章的默认分类
    'default_category': 'life',
    'posts_per_page': 10,

    # Mailgun Service
    'mailgun_key': '',
    'mailgun_enabled': 'no',

    # Mail
    'mail_from': ''
}
