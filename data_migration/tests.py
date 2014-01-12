# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.builtins import str

from django.test import TestCase, TransactionTestCase
from django.conf import settings
from django.contrib.auth.models import User, Group
from mock import patch

from .models import AppliedMigration
from .migration import Migration, Importer, Migrator

"""
Utility stuff
"""
def install_apps(apps):

    apps = [ "data_migration.test_apps.%s" % app for app in apps ]

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            with patch.object(Importer, 'installed_apps') as method:
                method.return_value = apps
                function(*args, **kwargs)

        return wrapper
    return real_decorator


"""
Test Cases
"""
class ImporterTest(TestCase):

    @install_apps(['valid_a', 'valid_b' 'missing_spec'])
    def test_import_existing_migrations_with_respect_to_excludes(self):
        Importer.import_all(excludes=["valid_b"])
        classes = Migration.__subclasses__()

        self.assertEqual(len(classes), 1)
        self.assertTrue("valid_a" in str(classes[0]))
        self.assertEqual(classes[0].model, User)

    @install_apps(['valid_a'])
    def test_that_decorator_works_as_expected(self):
        Importer.import_all()
        self.assertEqual(len(Migration.__subclasses__()), 1)


from .test_apps.blog.models import Blog, Category
from .test_apps.valid_a.data_migration_spec import UserMigration

class MigratorTest(TransactionTestCase):

    @install_apps(['valid_a', 'blog'])
    def test_topological_sorting(self):
        Importer.import_all()

        _sorted = Migrator.sorted_migrations()
        self.assertEqual(_sorted[0].model, User)
        self.assertEqual(_sorted[1].model, Blog)
        self.assertEqual(_sorted[2].model, Category)

    @patch.object(Migrator, 'sorted_migrations')
    def test_transaction_handling(self, sorted_migrations):
        sorted_migrations.return_value = [ UserMigration ]

        UserMigration.migrate = classmethod(
            lambda cls: AppliedMigration.objects.create(classname="test"))

        Migrator.migrate(commit=False)
        self.assertEqual(AppliedMigration.objects.count(), 0)

        Migrator.migrate(commit=True)
        self.assertEqual(AppliedMigration.objects.count(), 1)
