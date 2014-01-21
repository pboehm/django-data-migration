Welcome to django-data-migration's documentation!
=================================================

`django-data-migration` is a reusable Django app that migrates your legacy data
into your new django app. The only thing you have to supply is an appropriate
SQL query that transforms your data fromthe old schema into your model
structure. Dependencies between these migrations will be resolved
automatically. Give it a try!

.. warning:: This documentation is a work in progress. Please open an issue on
    Github if any information are missing.

Contents:
---------

.. toctree::
   :maxdepth: 3

   installing
   writing_migrations
   migrating
   troubleshooting

