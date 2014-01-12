from data_migration.migration import Migration
from django.contrib.auth.models import User, Group

class GroupMigration(Migration):
    model = Group
    depends_on = [ User ]
