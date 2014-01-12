from data_migration.migration import Migration
from django.contrib.auth.models import User

class UserMigration(Migration):
    model = User
