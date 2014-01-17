from data_migration.migration import Migration

from .models import Post, Comment, Author
from django.contrib.auth.models import User

class BaseMigration(Migration):

    @classmethod
    def open_db_connection(self):
        pass

class PostMigration(BaseMigration):
    query = "SELECT * FROM *;"
    model = Post
    depends_on = [ Author, Comment ]

class CommentMigration(BaseMigration):
    query = "SELECT * FROM *;"
    model = Comment
    depends_on = [ Author ]

class AuthorMigration(BaseMigration):
    query = "SELECT * FROM *;"
    model = Author
