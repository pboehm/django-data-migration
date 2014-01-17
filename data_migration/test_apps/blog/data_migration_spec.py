from data_migration.migration import Migration, is_a

from .models import Post, Comment, Author
from django.contrib.auth.models import User

import sqlite3
import os

class BaseMigration(Migration):

    @classmethod
    def open_db_connection(self):
        conn = sqlite3.connect(
                    os.path.join(os.path.dirname(__file__), 'blog_fixture.db'))

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        conn.row_factory = dict_factory
        return conn


class PostMigration(BaseMigration):
    query = """
    SELECT id,
        Title as title,
        Body as body,
        Posted as posted,
        Author as author,
        (
            SELECT
                GROUP_CONCAT(id)
            FROM comments c
            WHERE c.Post = p.id
        ) as comments
    FROM posts p;
    """
    model = Post
    depends_on = [ Author, Comment ]
    column_description = {
        'author': is_a(Author, search_attr="id", fk=True),
        'comments': is_a(Comment, search_attr="id", m2m=True, delimiter=",")
    }

    @classmethod
    def hook_after_save(self, instance, row):
        # because of the auto_now_add flag, we have to set it hard to this value
        instance.posted = row['posted']
        instance.save()


class CommentMigration(BaseMigration):
    query = """
    SELECT
        id,
        Message as message,
        Author as author,
        PostedAt as posted
    FROM comments;
    """
    model = Comment
    depends_on = [ Author ]
    column_description = {
        'author': is_a(Author, search_attr="id", fk=True),
    }

    @classmethod
    def hook_after_save(self, instance, row):
        # because of the auto_now_add flag, we have to set it hard to this value
        instance.posted = row['posted']
        instance.save()


class AuthorMigration(BaseMigration):
    query = """
    SELECT
        id,
        Firstname as firstname,
        Lastname as lastname,
        EmailAdress as email
    FROM authors;
    """
    model = Author

    @classmethod
    def hook_before_save(self, instance, row):
        # generate a username out of the lastname because it wasn't a username
        # in the old schema
        instance.username = row['firstname'].lower()
