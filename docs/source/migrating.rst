Migrating your data
===================

After you wrote all of your Migrations, you can put them in action by executing
the ``migrate_legacy_data`` management command::

    ./manage.py migrate_legacy_data [--commit]

If you omit the ``--commit``-flag, the data is not saved to the DB. This is
useful when you develop your migrations and have some failing migrations, but
the db is not cluttered with any incomplete data. When your migrations are
succesful you can add ``--commit`` and your data is saved when no errors occur.

.. note:: In older versions of this library, the management command is called
    ``migrate_this_shit``. This has been deprecated, but it is still there.
    ``migrate_legacy_data`` should be more appropriate.
