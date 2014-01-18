Writing Migrations
==================

Setup Database Connection
-------------------------

Write Your first Migration
--------------------------

Using Migration Hooks
---------------------

:class:`data_migration.migration.Migration` defines a number of different
hook-functions which will be called at different places allowing you to
customize the migration work at different levels.

.. autoclass:: data_migration.migration.Migration
   :members: hook_before_all, hook_before_transformation, hook_before_save, hook_after_save, hook_after_all, hook_update_existing
