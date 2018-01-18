# coding=utf-8

import os
import os.path
import zipfile
import datetime
import random
import sqlite3
import string
from vanellope import config
print '#### ', config.app_settings

create_table_sqls = config.create_table_sqls

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

def create_tables():
    # Create tables if not exist
    cur = connection.cursor()

    # Create configuration table
    cur.execute(create_table_sqls['conf_schema'])
    cur.execute('SELECT * FROM configuration')
    results = cur.fetchall()

    # Initialize configurations
    if len(results) == 0:
        t = config.app_settings.items()
        cur.executemany("INSERT INTO configuration VALUES (?, ?)", t)

    # Create posts table
    cur.execute(create_table_sqls['posts_schema'])

    # Create users schema
    cur.execute(create_table_sqls['users_schema'])

    # Create comments schema
    cur.execute(create_table_sqls['comments_schema'])

    # Create comments schema
    cur.execute(create_table_sqls['posts_views_schema'])


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


