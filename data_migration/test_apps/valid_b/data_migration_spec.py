from data_migration.migration import Migration
from django.contrib.auth.models import User, Group

class GroupMigration(Migration):
    query = "SELECT * FROM users;"
    model = Group
    depends_on = [ User ]
