# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins import str

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models import Model

from .models import AppliedMigration
from .utils import itersubclasses

import inspect
import sys
import inspect
import re

def is_a(klass=None, search_attr=None, fk=False, m2m=False, o2o=False,
                exclude=False, delimiter=';', skip_missing=False):
    """
    Generates a uniform set of information out of the supplied data and does
    some validations. This function is used to build the `column_description`
    attribute in your migration. The information is used to translate your data
    from the old DB schema into django instances.

    :param klass: A model class which has a reference to the current column
    :param search_attr: A model attribute which is used to filter for the right
                        model instance
    :param fk: The specified column in query includes a ForeinKey-Reference
    :param m2m: The specified column in query includes (possible multiple)
                elements which will be represented by a ManyToMany-Reference
    :param delimiter: The character which separates multiple elements in a
                      `m2m`-column
    :param o2o: The specified column in query includes a OneToOne-Reference
    :param exclude: The specified column should not be processed automatically,
                    but can be accessed in any hook which includes the
                    `row`-parameter
    :param skip_missing: defines the behaviour if any element in a defined
                         relation (`fk`, `m2m` or `o2o`) can not be found. If
                         set to `True`, missing elements are ignored. Otherwise
                         an exception is raised.
    """

    if exclude is not True:

        if not (klass and search_attr):
            raise ImproperlyConfigured(
                'you have to specify at least `klass`, `search_attr` and '
                'a type of relation')

        if not (inspect.isclass(klass) and issubclass(klass, Model) ):
            raise ImproperlyConfigured(
                'you have to specify a subclass of Model as `klass`')

        if len([ e for e in [fk, m2m, o2o] if e ]) != 1:
            raise ImproperlyConfigured('a column has to be either `fk`, `m2m` or `o2o`')

    return { 'm2m': m2m, 'klass': klass, 'fk': fk, 'o2o': o2o,
             'attr': search_attr, 'exclude': exclude, 'delimiter': delimiter,
             'skip_missing': skip_missing,
            }


class Migration(object):
    """Baseclass for each data migration"""

    #: If `True`, this migration will be skipped and not processed.
    skip = False

    #: The Django model class there the query creates instances for. There
    #: could be only one migration for each model.
    model = None

    #: An SQL-SELECT-query which returns the data that is processed and passed
    #: to the model-class-constructor. Please consult the documentation for an
    #: in-depth description for this attribute.
    query = None

    #: This dict contains information about special columns returned by the
    #: query (ForeinKey-, OneToOne- and Many2Many-Relations) or if it should be
    #: excluded from automatic processing.
    column_description = {}

    #: A list of model classes the model requires to be migrated before itself.
    #: This includes normally all model classes which are listed in
    #: `column_description`.
    depends_on = []

    #: If the following is set to `False`, the migration will be executed only
    #: once. Otherwise it will search for missing elements and creates them.
    allow_updates = False

    #: This is a unique model field, which is used to search for existing
    #: model instances.
    #:
    #: Example: for Django`s User model it can be `username` or `id`
    #:
    #: :important: this attribute is required if `allow_updates` is set to
    #:             `True`
    search_attr = None

    #########
    # Hooks #
    #########
    @classmethod
    def hook_before_transformation(self, row):
        """Is called right before row is passed to the model constructor.

        Manipulate the row data if it is required. Here you can bring the data
        in a suitable form which is not possible in SQL itself.

        :param row: the dict which represents one row of the SQL query
        """
        pass


    @classmethod
    def hook_before_save(self, instance, row):
        """Is called right before the migrated instance is saved.

        Do the changes, that make the instance valid, in this hook.

        :param instance: the migrating instance which could be altered
        :param row: the dict which represents one row of the SQL query
        """
        pass


    @classmethod
    def hook_after_save(self, instance, row):
        """Is called right after the migrated instance has been saved initially.

        This is the place where you can set the data for a DateTimeField with
        `auto_now_add`, where the date from the SQL query is not used
        otherwise.

        :param instance: the migrating instance which could be altered
        :param row: the dict which represents one row of the SQL query
        :note: when you make changes to the instance you have to call `save()`
               manually
        """
        pass


    @classmethod
    def hook_update_existing(self, instance, row):
        """Is called for each existing instance when `allow_updates` is True

        :param instance: the existing instance which can be updated
        :param row: contains the raw result without any transformation

        :note: It is YOUR responsibility to make sure, that this method can be
               called MULTIPLE times. DO SOME CHECKS
        """
        pass


    @classmethod
    def hook_before_all(self):
        """Is called before the migration will be migrated

        Here you can execute some special setup code, which should be executed
        only once.
        """
        pass


    @classmethod
    def hook_after_all(self):
        """Is called after the migration has been processed succesfully

        Here you can set a debugger breakpoint for testing the migration
        results.
        """
        pass


    ###################
    # INTERNAL THINGS #
    ###################
    @classmethod
    def migrate(self):
        """method that is called to migrate this migration"""

        check = self.migration_required()
        if check == False:
            print("%s has already been migrated, skip it!" % self)
            return None

        print("Migrating %s" % self)

        self.check_migration() # check the configuration of the Migration
        connection = self.open_db_connection()

        cursor = connection.cursor()
        cursor.execute(self.query)
        fields = [ row[0] for row in cursor.description ]

        if check is None:
            # update existing migrations
            self.process_cursor_for_update(cursor, fields)

        else:
            # do the normal migration method
            self.process_cursor(cursor, fields)

            AppliedMigration.objects.create(classname=str(self))


    @classmethod
    def open_db_connection(self):
        raise ImproperlyConfigured(
            "You have to supply a suitable db connection for your DB: %s" % self)


    @classmethod
    def process_cursor(self, cursor, fields):
        total = cursor.rowcount
        current = 0

        self.hook_before_all()

        for row in cursor.fetchall():

            current += 1
            sys.stdout.write("\rMigrating element %d/%d" % (current, total))
            sys.stdout.flush()

            self.hook_before_transformation(row)
            constructor_data, m2ms = self.transform_row_dataset(row)
            instance = self.model(**constructor_data)

            self.hook_before_save(instance, row)

            instance.save()

            self.create_m2ms(instance, m2ms)

            self.hook_after_save(instance, row)

        self.hook_after_all()
        print("")


    @classmethod
    def process_cursor_for_update(self, cursor, fields):
        total = cursor.rowcount
        created = 0
        existing = 0

        for row in cursor.fetchall():

            # search for an existing instance
            desc = is_a(self.model, search_attr=self.search_attr,
                        fk=True, skip_missing=True)
            element = self.get_object(desc, row[self.search_attr])

            if element is not None:
                existing += 1
            else:
                created += 1

            sys.stdout.write(
                "\rSearch for missing Instances (exist/created/total):  %d/%d/%d" % (
                    existing, created, total))
            sys.stdout.flush()

            if element is not None:
                self.hook_update_existing(element, row)
                continue

            self.hook_before_transformation(row)
            constructor_data, m2ms = self.transform_row_dataset(row)
            instance = self.model(**constructor_data)

            self.hook_before_save(instance, row)

            instance.save()

            self.create_m2ms(instance, m2ms)

            self.hook_after_save(instance, row)

        print("")


    @classmethod
    def transform_row_dataset(self, datarow):
        """transforms the supplied row and evaluates columns of different types

        returns the dict where columns which FKs or Data has been updated with
        real instances
        """
        constructor_data = {}
        m2ms = {}

        for fieldname, data in datarow.items():
            if fieldname in self.column_description:
                desc = self.column_description[fieldname]

                if desc['exclude'] == True:
                    continue

                elif desc['fk'] == True or desc['o2o'] == True:
                    instance = self.get_object(desc, data)
                    constructor_data[fieldname] = instance

                elif desc['m2m'] == True:
                    if data is None:
                        continue

                    parts = data.split(desc['delimiter'])
                    objects = []

                    for part in parts:
                        element = self.get_object(desc, part)
                        if element is None:
                            continue
                        objects.append(element)
                    m2ms[fieldname] = objects

            else:
                constructor_data[fieldname] = data

        return (constructor_data, m2ms,)


    @classmethod
    def get_object(self, desc, value):
        criteria = { desc['attr']: value }
        try:
            return desc['klass'].objects.get(**criteria)
        except self.model.DoesNotExist as e:
            if desc['skip_missing']:
                return None
            else:
                raise


    @classmethod
    def create_m2ms(self, instance, m2ms):
        for field, values in m2ms.items():
            instance.__getattribute__(field).add(*values)


    @classmethod
    def migration_required(self):
        """checks if the migration has already been applied"""
        try:
            AppliedMigration.objects.get(classname=str(self))

            if self.allow_updates:
                return None

            return False
        except AppliedMigration.DoesNotExist as e:
            return True


    @classmethod
    def check_migration(self):

        if not isinstance(self.column_description, dict):
            raise ImproperlyConfigured(
                    '%s: `column_description` has to be a dict' % self)

        if self.allow_updates and self.search_attr is None:
            raise ImproperlyConfigured(
                    '%s: `allow_updates` forces you to set the `search_attr` on ' % self +
                    'the Migration. to search for existing instances. Example: `username`')

        if not isinstance(self.depends_on, list):
            raise ImproperlyConfigured(
                    '%s: `depends_on` has to be a list of classes' % self)

        if not ( inspect.isclass(self.model) and issubclass(self.model, Model)):
            raise ImproperlyConfigured(
                    '%s: `model` has to be a model CLASS' % self)

        if not re.search('SELECT', self.query, re.IGNORECASE|re.MULTILINE):
            raise ImproperlyConfigured(
                '%s: `query` has to be a string containing SELECT: %s' % (
                    self, self.query))


from django.conf import settings

class Importer(object):
    """
    this class encapsulates all the logic it needs to find all existing data
    migrations accross all installed apps
    """

    @classmethod
    def installed_apps(self):
        return settings.INSTALLED_APPS

    @classmethod
    def possible_existing_migrations(self):
        return [ app + ".data_migration_spec"
            for app in self.installed_apps() ]

    @classmethod
    def import_all(self, excludes=[]):
        """
        this does an `from X import *` for all existing migration specs
        """
        for app in self.possible_existing_migrations():

            matches = [ ex for ex in excludes if ex in app ]
            if len(matches) > 0:
                continue

            try:
                m = __import__(app)
                try:
                    attrlist = m.__all__
                except AttributeError:
                    attrlist = dir(m)

                for attr in attrlist:
                    globals()[attr] = getattr(m, attr)

            except ImportError as e:
                pass


class NotCommitBreak(Exception):
    pass


from django.db import transaction
import networkx as nx

class Migrator(object):
    """
    this class encapsulates the migration process for all existing migration
    classes. This is normally used by the migrate_this_shit management command
    """

    @classmethod
    def migrate(self, commit=False, log_queries=False):
        try:
            with transaction.commit_on_success():
                for migration in self.sorted_migrations():

                    if migration.skip is True:
                        print("%s: will be skipped" % migration)
                        continue

                    if log_queries:
                        print(("Query for %s: " % (migration)) + migration.query)

                    migration.migrate()

                if not commit:
                    raise NotCommitBreak("nothing has changed")

        except NotCommitBreak as e:
            pass


    @classmethod
    def sorted_migrations(self):
        return self.sort_based_on_dependency(
            [ mig for mig in itersubclasses(Migration) if mig.query ])


    @classmethod
    def sort_based_on_dependency(self, classes):
        """sorts the given Migration classes based on their dependencies
            to other Models.

        returns a list of MigrationClasses in the order they can be migrated
        or raises suitable exceptions if this couldn't be completed
        """

        def topological_sort(edges):
            """
            does a topological sort on the supplied edges http://goo.gl/lkOt1
            """
            G = nx.DiGraph()
            for path in edges:
                G.add_nodes_from(path)
                G.add_path(path)
            return nx.topological_sort(G)


        # get a migratable order of models which are specified in the migrations
        dependency_graphs = [ mig.depends_on + [ mig.model ]
                                for mig in classes ]

        ordered_models = topological_sort(dependency_graphs)
        ordered_migrations = []

        # sort the migrations and do some checks
        for model in ordered_models:
            matching_mig = [ cla for cla in classes if cla.model == model ]

            if len(matching_mig) == 1:
                ordered_migrations.append(matching_mig[0])
            elif len(matching_mig) == 0:
                raise AttributeError(
                    "There is no migration available for '%s'" % model)
            else:
                raise AttributeError(
                    "InvalidState: '%s' has more than one migration" % model)

        return ordered_migrations
