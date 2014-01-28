Writing Migrations
==================

What is a Migration?
--------------------

A migration is a Python class that should be placed in a file called
``data_migration_spec.py`` in one of your app-directories.
``django-data-migrations`` searches in each app, included in
``INSTALLED_APPS``, for this file and imports all from it automatically.

**Your migration normally specifies the following things:**

* A database connection to your legacy data (whereever this is)
* The model class, the migration should create instances for
* A corresponding SQL-Query, which maps the old DB-schema to the new
  Django-model-schema

    * You can specify what should be done with special columns, returned by the
      query (Many2Many-, ForeignKey-, One2One-Relations). With minimal
      configuration, these things can be migrated automatically.

* Dependencies to other models can be specified. This is used, to determine the
  order each migration can be applied. e.g. If a migration specifies
  a model as dependency, his migration will be executed before our migration
  will be processed.
* You can implement different hooks, where you normally manipulate the data
  returned by the query or do some things which are not possible by SQL itself.
* You can specify, if your migration should look for new instances on a second
  run. This is not the default case.

.. _complete_example:

A complete Migration example
----------------------------

To give you an overview, how a common migration looks, the following listing
shows a migration for a ``Post`` model. This is an excerpt from a
``data_migration_spec.py`` which can be found in a testing app, which is used by
``django-data-migration`` itself.

`The complete app can be found here ...
<https://github.com/pboehm/django-data-migration/tree/master/data_migration/test_apps/blog>`_

.. literalinclude:: ../../data_migration/test_apps/blog/data_migration_spec.py
    :pyobject: PostMigration

As you can see, ``PostMigration`` inherits from a class called ``BaseMigration``.
This is one of the classes which is listed here :ref:`db_connection_setup`.


Migration details
-----------------

.. _db_connection_setup:

Setup Database Connection
*************************

``django-data-migration`` should support as many databases as possible, so the
connection part is not implemented directly for each database. You have to
override the ``open_db_connection`` classmethod in your migration.

.. tip:: The connection handling should be implemented once in a
         ``BaseMigration`` where all other Migrations inherit from.

.. important:: ``django-data-migration`` requires that the database returns a
               ``DictCursor``, where each row is a dict with column names as keys
               and the row as corresponding values.

SQLite
......

The following code implements an example database connection for SQLite:

.. code-block:: python

    import sqlite3

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            conn = sqlite3.connect(......)

            def dict_factory(cursor, row):
                d = {}
                for idx, col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d

            conn.row_factory = dict_factory
            return conn


MySQL
......

You have to install the corresponding MySQL-Python-driver by executing::

    pip install MySQL-python

The following code implements an example database connection for MySQL.

.. code-block:: python

    import MySQLdb

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            return MySQLdb.connect(......,
                cursorclass=MySQLdb.cursors.DictCursor
            )


PostgreSQL
..........

You have to install the corresponding PostgreSQL-Python-driver by executing::

    pip install psycopg2

The following code implements an example database connection for PostgreSQL.

.. code-block:: python

    import psycopg2

    class BaseMigration(Migration):

        @classmethod
        def open_db_connection(self):
            return psycopg2.connect(......,
                cursor_factory=psycopg2.extras.DictCursor
            )


What can be configured in every migration
*****************************************

In your migration classes you have several configuration options, which are
listed below with a short description. For an in-depth explanation you can
consult the paragraphs below.

.. module:: data_migration.migration

.. autoattribute:: Migration.skip
.. autoattribute:: Migration.query
.. autoattribute:: Migration.model
.. autoattribute:: Migration.depends_on
.. autoattribute:: Migration.column_description
.. autoattribute:: Migration.allow_updates
.. autoattribute:: Migration.search_attr

Writing effective Migration-queries
***********************************

.. important:: TODO

Define dependencies
*******************

.. important:: TODO

Describe special columns
************************

Your ``query`` can include special columns, that are represented as special
Django-relations (ForeignKey-, Many2Many- or One2One-Relations). Or you can
exclude specific columns from automatic processing. You will normally define
these settings with an invocation of the ``is_a``-function, which does some tests
and returns the required settings. This will then be used by
``django-data-migration`` in different places.

.. autofunction:: is_a

Some examples for ``is_a`` can be found here: :ref:`complete_example`.

Using Migration Hooks
*********************

:class:`data_migration.migration.Migration` defines a number of different
hook-functions which will be called at different places allowing you to
customize the migration work at different levels.

.. autoclass:: data_migration.migration.Migration
   :members: hook_before_all, hook_before_transformation, hook_before_save, hook_after_save, hook_after_all, hook_update_existing

Hook-Flowchart
..............

The following graphic shows each Hook-method and when it is called in contrast
to the model handling which is done by ``django-data-migration``.

::

    +------------------+
    |hook_before_all() |
    +--------------+---+
                   |
        +-----+    |
        |     |    |
        |  +--v----v--------------------+
        |  |hook_before_transformation()|
        |  +-------+--------------------+
        |          |
        |      +---v--------------------+
        |      |instance = model(**data)|
        |      +---+--------------------+
        |          |
        |  +-------v----------+
        |  |hook_before_save()|
        |  +-------+----------+
        |          |
        |      +---v-----------+
        |      |instance.save()|
        |      +---+-----------+
        |          |
        |  +-------v---------+
        |  |hook_after_save()|
        |  +-------+---------+
        |          |
        +-------+--+
                |
                |
    +-----------v-----+
    |hook_after_all() |
    +-----------------+


Implement updateable Migrations
*******************************

.. important:: TODO
