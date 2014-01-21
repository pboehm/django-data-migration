django-data-migration
=====================
[![PyPi version](https://pypip.in/v/django-data-migration/badge.png)](https://crate.io/packages/django-data-migration/)
[![PyPi downloads](https://pypip.in/d/django-data-migrtion/badge.png)](https://crate.io/packages/django-data-migration/)
[![Build Status](https://travis-ci.org/pboehm/django-data-migration.png?branch=master)](https://travis-ci.org/pboehm/django-data-migration)

`django-data-migration` is a reusable Django app that migrates your legacy data
into your new django app. The only thing you have to supply is an appropriate
SQL query that transforms your data from the old schema into your model
structure. Dependencies between these migrations will be resolved
automatically. Give it a try!

This extension is tested automatically against:

* Django 1.5
* Django 1.6

on Python 2.7 and 3.3.

Python 3.2 is not supported, due to a [SyntaxError in the
future library](https://github.com/PythonCharmers/python-future/issues/29)
which is used to support both Python 2 and 3.

## Installation

1. Install using pip:

    ```
    pip install django-data-migration
    ```

2. Add to `INSTALLED_APPS`:

    ```
    'data_migration',
    ```

3. Run `./manage.py migrate` or `./manage.py syncdb` to create the included
   models

Alternatively, you can add `django-data-migration` to your `requirements.txt`.

## Documentation

The documentation of `django-data-migration` is built by `sphinx` and can be
edited in the `docs/` directory of this project.

[Go to the Documentation on Read The Docs](http://django-data-migration.readthedocs.org/en/latest/)

## Status of project

This app has been extracted out of a production system and some work has been
done, to write tests and refactor code. The project documentation is a work in
progress.

## Start participating

* Fork the project on Github and clone it locally
* Install Python 2.7 and 3.3, `virtualenv` and `tox`
* Run the tests with `tox` against all supported versions of Python
* Create a Pull Request on Github
