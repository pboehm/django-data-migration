# -*- coding: utf-8 -*-
from django.test import TestCase
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
        self.assertTrue("valid_a" in unicode(classes[0]))
        self.assertEqual(classes[0].model, User)

    @install_apps(['valid_a'])
    def test_that_decorator_works_as_expected(self):
        Importer.import_all()
        self.assertEqual(len(Migration.__subclasses__()), 1)


class MigratorTest(TestCase):

    @install_apps(['valid_a', 'valid_b'])
    def test_topological_sorting(self):
        Importer.import_all()

        _sorted = Migrator.sorted_migrations()
        self.assertEqual(_sorted[0].model, User)
        self.assertEqual(_sorted[1].model, Group)

