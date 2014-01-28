Installing
==========

Installation of ``django-data-migration`` is straight forward, as it only
requires the following steps (assuming you have already set up ``virtualenv``
and ``pip``).

1) Install using pip::

    pip install django-data-migration

2) Add ``django-data-migration`` to your ``requirements.txt``

3) Add to ``INSTALLED_APPS``::

    'data_migration',

4) Run ``./manage.py migrate`` or ``./manage.py syncdb`` to create the included
   models
