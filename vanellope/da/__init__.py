# coding=utf-8

import os
import os.path
import zipfile
import datetime
import random
import sqlite3
import string
from vanellope import config

create_table_sqls = config.create_table_sqls
app_settings = config.app_settings

# Autocommit ON
connection = sqlite3.connect(
    config.db_path,
    isolation_level=None,
    detect_types=sqlite3.PARSE_DECLTYPES
)
session_connection = sqlite3.connect(':memory:')


def record_view(post_id):
    # TODO is special id ?
    cur = connection.cursor()

    update_sql = 'UPDATE views SET counts = counts + 1 WHERE post_id = ? LIMIT 1'
    insert_sql = 'INSERT INTO views (post_id, counts) VALUES (?, ?)'
    result = cur.execute(update_sql, post_id)
    if not result.count:
        cur.execute(insert_sql, [post_id, 0])

    # TODO check is post_id exist
    # if exist, then update counts
    # if not, insert one,

def init_db():
    """Initialize database or update db tables structure
    """
    cur = connection.cursor()

    for sql in create_table_sqls:
        cur.execute(sql)

    # Initialize configurations
    cur.executemany("INSERT OR IGNORE INTO configuration VALUES (?, ?)", app_settings.items())

    fixtures()

def fixtures():
    """
    """
    cur = connection.cursor()

    # Add new field in posts_schema
    try:
        cur.execute('ALTER TABLE posts ADD COLUMN summary TEXT DEFAULT ""')
    except:
        pass

    try:
        cur.execute('ALTER TABLE posts ADD COLUMN hero TEXT DEFAULT ""')
    except:
        pass

    connection.commit()

def db_backup():
    current_time_str = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%ZZ')
    filename = '.'.join([current_time_str, 'sql'])
    full_path = os.path.join(config.backup_path, filename)
    dump = os.linesep.join(connection.iterdump())

    zip_path = full_path + '.zip'
    zip_filename = filename + '.zip'

    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zf.writestr(filename, dump.encode('utf-8'))
    zf.close()

    return zip_path, zip_filename


def random_string(n):
    string_set = string.ascii_letters + string.digits + "!@#$%^&*<>?{}[]"
    return ''.join(random.choice(string_set) for _ in range(n))


class DataAccess(object):
    """读取数据库的通用方法集
    """

    # Get Database Connection
    @property
    def conn(self):
        return connection

    def to_dict(self, cur, row):
        """Convert SQLite3 results to dict

           http://stackoverflow.com/questions/3300464
        """
        if not row:
            return

        d = {}
        for idx, col in enumerate(cur.description):
            d[col[0]] = row[idx]
        return d

    def get_admin(self):
        """Get master user
        """

        cur = self.conn.cursor()
        cur.execute("""
            SELECT * from users WHERE role = "master";
        """)
        master = cur.fetchone()
        return master


