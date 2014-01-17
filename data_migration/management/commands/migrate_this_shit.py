# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError, make_option
from django.utils import translation
from django.conf import settings

from data_migration.migration import Importer, Migrator

class Command(BaseCommand):
    help = 'Migrates old data into the new django schema'
    can_import_settings = True

    option_list = BaseCommand.option_list + (
        make_option('--commit',
            action='store_true',
            help='Commits the Changes to DB if all migrations are done right.',
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
            help='Print the corresponding Query for each migration.',
            dest='logquery',
            default=False),
    )

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        excluded_apps = options.get('excluded_apps', [])
        Importer.import_all(excludes=excluded_apps)

        Migrator.migrate(
            commit=options.get('commit_changes', False),
            log_queries=options.get('logquery', False)
        )
