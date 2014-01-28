Migrating your data
===================

After you wrote all of your Migrations, you can put them in action by executing
the ``migrate_this_shit`` management command::

    ./manage.py migrate_this_shit [--commit]

If you omit the ``--commit``-flag, the data is not saved to the DB. This is
useful when you develop your migrations and have some failing migrations, but
the db is not cluttered with any incomplete data. When your migrations are
succesful you can add ``--commit`` and your data is saved when no errors occur.
