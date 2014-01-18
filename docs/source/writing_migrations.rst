Writing Migrations
==================

Setup Database Connection
-------------------------

`django-data-migration` should support as many databases as possible, so the
connection part is not implemented directly for each database. You have to
override the `open_db_connection` classmethod in your migration.

.. tip:: The connection handling should be implemented once in a
         `BaseMigration` where all other Migrations inherit from.

.. important:: `django-data-migration` requires that the database returns a
               `DictCursor`, where each row is a dict with column names as keys
               and the row as corresponding values.

SQLite
......

The following code implements an example database connection for SQLite:

.. code-block:: python

    import sqlite3

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            conn = sqlite3.connect(':memory:'))

            def dict_factory(cursor, row):
                d = {}
                for idx, col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d

            conn.row_factory = dict_factory
            return conn


MySQL
......

You have install the corresponding MySQL-Python-driver by executing::

    pip install MySQL-python

The following code implements an example database connection for MySQL.

.. code-block:: python

    import MySQLdb

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            return MySQLdb.connect(
                host=HOST, user=USER, passwd=PASSWORD,
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True
            )


PostgreSQL
..........

You have install the corresponding PostgreSQL-Python-driver by executing::

    pip install psycopg2

The following code implements an example database connection for PostgreSQL.

.. code-block:: python

    import psycopg2

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            return psycopg2.connect(...,
                        cursor_factory=psycopg2.extras.DictCursor)


Write Your first Migration
--------------------------

Using Migration Hooks
---------------------

:class:`data_migration.migration.Migration` defines a number of different
hook-functions which will be called at different places allowing you to
customize the migration work at different levels.

.. autoclass:: data_migration.migration.Migration
   :members: hook_before_all, hook_before_transformation, hook_before_save, hook_after_save, hook_after_all, hook_update_existing
