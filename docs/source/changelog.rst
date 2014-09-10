.. currentmodule:: data_migration.Migration

Changelog
=========

Version 0.2.1
+++++++++++++

* ``atomic()`` is now used instead of ``commit_on_success()`` when it is
  available. This prevents deprecation warnings that are displayed with Django
  >= 1.7.

Version 0.2.0
+++++++++++++

* Introduced some performance improvements by implementing prefetching of
  related objects, that reduces the number of issued SQL-Queries dramatically.
  There is now the opportunity to assign related objects by their id instead of
  a full instance, which can reduce the memory usage.
* There are two new arguments in ``is_a``: ``prefetch=True`` and
  ``assign_by_id=False``. Because prefetching is enabled by default, it
  should bring a massive performance boost only by upgrading to this version
* Switching to a new minor release because of the changed behaviour in
  ``get_object``


Version < 0.2.0
+++++++++++++++

There is no explicit Changelog until 0.2.0. Use ``git log`` to get the
information from git.
