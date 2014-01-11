# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError, make_option
from django.db import transaction
from django.utils import translation
from django.conf import settings

from settings import SITE_ROOT

from .migration import Migration
from .utils import itersubclasses

import networkx as nx
import sys
import os

class NotCommitBreak(Exception):
    pass

class Command(BaseCommand):
    help = 'Migrates old data into the new django schema'
    can_import_settings = True

    option_list = BaseCommand.option_list + (
        make_option('--commit',
            action='store_true',
            help='Commit the Changes to DB if the migrations are done right.',
            dest='commit_changes',
            default=False),
        make_option('--exclude',
            action='append',
            metavar='APP',
            help='Excludes the supplied app from beeing migrated.',
            dest='excluded_apps',
            default = []),
        make_option('--logquery',
            action='store_true',
            help='Print the corresponding Query for each database.',
            dest='logquery',
            default=False),
    )

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        def get_support2_apps():
            """generates a list of all app names included in support2"""
            apps = []

            for entry in os.listdir(SITE_ROOT):
                if os.path.isfile( os.path.join(SITE_ROOT, entry, "models.py")):
                    apps.append("support2.%s" % entry)

            return apps


        def import_all_migrations(excludes=[]):
            apps = [ app + ".data_migration" for app in get_support2_apps() ]

            for app in apps:

                matches = [ ex for ex in excludes if str(ex) in app ]
                if len(matches) != 0:
                    print "%s: has been excluded" % app
                    continue

                try:
                    m = __import__ (app)
                    try:
                        attrlist = m.__all__
                    except AttributeError:
                        attrlist = dir (m)
                    for attr in attrlist:
                        globals()[attr] = getattr (m, attr)

                    print "Found migrations in '%s'" % app
                except ImportError, e:
                    print "%s: %s" % (app, e)


        def sort_based_on_dependency(classes):
            """sorts the given Migration classes based on their dependencies
               to other Models.

            returns a list of MigrationClasses in the order they can be migrated
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

            dependency_graphs = [ mig.depends_on + [ mig.model ]
                                    for mig in classes ]

            ordered_models = topological_sort(dependency_graphs)
            ordered_migrations = []

            for model in ordered_models:
                matching_mig = [ cla for cla in classes if cla.model == model ]
                if len(matching_mig) == 1:
                    ordered_migrations.append(matching_mig[0])
                elif len(matching_mig) == 0:
                    raise AttributeError(
                        "There is no migration for '%s' available" % model)
                else:
                    raise AttributeError(
                        "InvalidState: '%s' has more than one migration" % model)

            return ordered_migrations


        @transaction.commit_on_success
        def migrate_migrations(migrations, commit=False, logquery=False):

            for migration in sorted_migrations:
                if migration.skip is True:
                    print "%s: will be skipped" % migration
                    continue

                if logquery:
                    print ("Query for %s: " % (migration)) + migration.query
                migration.migrate()

            if not commit:
                raise NotCommitBreak("nothing has changed")

        excluded_apps = options.get('excluded_apps', [])
        import_all_migrations(excluded_apps)
        print ""

        migrations = [ klass for klass in itersubclasses(Migration)
                             if klass.abstract == False ]
        sorted_migrations = sort_based_on_dependency(migrations)

        try:
            migrate_migrations(sorted_migrations,
                    options.get('commit_changes', False),
                    options.get('logquery', False)
                    )
        except NotCommitBreak, e:
            print "\nNot commiting. Add --commit to save your changes."
