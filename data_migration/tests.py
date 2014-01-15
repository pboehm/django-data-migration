# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.builtins import str

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User, Group
from mock import patch

from .models import AppliedMigration
from .migration import is_a, Migration, Importer, Migrator

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


class IsATest(TestCase):

    def test_normal_description(self):
        self.assertEqual(is_a(User, 'username', fk=True), {
            'klass': User,
            'attr': 'username',
            'm2m': False,
            'delimiter': u';',
            'skip_missing': False,
            'o2o': False,
            'exclude': False,
            'fk': True,
        })

    def test_that_class_and_attr_has_to_be_present(self):
        with self.assertRaises(ImproperlyConfigured):
            is_a(fk=True)

    def test_that_class_has_to_be_a_model(self):
        with self.assertRaises(ImproperlyConfigured):
            is_a(str(User), 'username', fk=True)

    def test_multiple_type_definition(self):
        with self.assertRaises(ImproperlyConfigured):
            is_a(User, 'username', fk=True, m2m=True)

    def test_exclude_from_processing(self):
        self.assertEqual(is_a(exclude=True), {
            'klass': None,
            'attr': None,
            'm2m': False,
            'delimiter': u';',
            'skip_missing': False,
            'o2o': False,
            'exclude': True,
            'fk': False,
        })
