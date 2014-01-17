# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.builtins import str

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User, Group
from mock import patch
from io import StringIO

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
        old_count = len(Migration.__subclasses__())
        Importer.import_all(excludes=["valid_b"])
        new_count = len(Migration.__subclasses__())

        self.assertEqual(new_count - old_count, 1)


from .test_apps.blog.models import Author, Post, Comment
from .test_apps.blog.data_migration_spec import *

class MigratorTest(TransactionTestCase):

    @install_apps(['valid_a', 'blog'])
    def test_that_no_abstract_migration_will_be_sorted_in(self):
        Importer.import_all()

        _sorted = Migrator.sorted_migrations()
        self.assertFalse(BaseMigration in _sorted)


    @install_apps(['valid_a', 'blog'])
    def test_topological_sorting(self):
        Importer.import_all()

        _sorted = Migrator.sort_based_on_dependency(
                    [AuthorMigration, PostMigration, CommentMigration])
        self.assertEqual(_sorted[0].model, Author)
        self.assertEqual(_sorted[1].model, Comment)
        self.assertEqual(_sorted[2].model, Post)


    @patch.object(Migrator, 'sorted_migrations')
    def test_transaction_handling(self, sorted_migrations):
        sorted_migrations.return_value = [ AuthorMigration ]

        AuthorMigration.migrate = classmethod(
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

import os
import sqlite3

class MigrationTest(TransactionTestCase):

    def setUp(self):
        self.db_path = os.path.join(
                os.path.dirname(__file__), 'test_apps/blog/blog_fixture.db')

        if not os.path.isfile(self.db_path):
            fixture = os.path.join(os.path.dirname(self.db_path), "fixtures.sql")
            conn = sqlite3.connect(self.db_path)
            conn.cursor().executescript(open(fixture).read())
            conn.close()

    def tearDown(self):
        if os.path.isfile(self.db_path):
            os.unlink(self.db_path)

    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(Migration, '__subclasses__')
    def test_description(self, subclasses, stdout):
        subclasses.return_value = [
            BaseMigration, AuthorMigration, PostMigration, CommentMigration
        ]

        Migrator.migrate()
        self.assertTrue(True)

