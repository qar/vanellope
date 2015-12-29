#! /usr/bin/env python
# coding=utf-8

"""
Default configurations.
Those can be overide by user specify settings
"""

import os
import os.path

# The theme name
theme = 'default'

# How many post displayed on one page
posts_per_page = 10

# SQLite3 Settings
db_path = os.path.join(os.getcwd(), u'content/data.db')

if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# 数据库备份目录
backup_path = os.path.join(os.getcwd(), u'content/backups/')
if not os.path.exists(os.path.dirname(backup_path)):
    os.makedirs(os.path.dirname(backup_path))

# 上传文件的存储路径
# 绝对路径
uploaded_path = os.path.join(os.getcwd(), u'content/www/')

if not os.path.exists(os.path.dirname(uploaded_path)):
    os.makedirs(os.path.dirname(uploaded_path))

create_table_sqls = {
    "posts_schema": """
                    CREATE TABLE IF NOT EXISTS posts (
                         uuid TEXT PRIMARY KEY,
                         ext TEXT,
                         title TEXT,
                         content TEXT,
                         category TEXT NOT NULL,
                         tags TEXT,
                         state TEXT NOT NULL DEFAULT 'published',
                         created_at TIMESTAMP NOT NULL,
                         updated_at TIMESTAMP NOT NULL
                    )
                    """,

    "users_schema": """
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        email TEXT UNIQUE,
                        passwd TEXT,
                        salt TEXT,
                        role TEXT,
                        created_at NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """,

    "conf_schema": """
                    CREATE TABLE IF NOT EXISTS configuration (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                    """
}

app_settings = {
    # 网站标题
    'site_title': 'Life with vanellope',

    # 网站地址 like 「www.example.com」
    'site_url': '',

    # 网站统计服务
    'site_tracking': '', # 'google_analystics'
    'site_tracking_id': '',
    'site_tracking_enabled': 'yes',

    # 网站评论服务
    'site_comment': '' , # 'duoshuo' or 'disqus'
    'site_comment_id': '' ,
    'site_comment_enabled': 'no',

    # Post default category
    # 新建文章的默认分类
    'default_category': 'life',

    # draft url: http://www.example.com/drafts/<uuid>+title
    'draft_base_path': '/drafts/'
}
