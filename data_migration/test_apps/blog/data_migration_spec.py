from data_migration.migration import Migration

from .models import Blog, Category
from django.contrib.auth.models import User

class BlogMigration(Migration):
    model = Blog
    depends_on = [ User ]

class CategoryMigration(Migration):
    model = Category
    depends_on = [ Blog ]
