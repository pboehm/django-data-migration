django-data-migration [![Build Status](https://travis-ci.org/pboehm/django-data-migration.png?branch=master)](https://travis-ci.org/pboehm/django-data-migration)
=====================

`django-data-migration` is a reusable Django app that migrates your legacy data
into your new django app. The only thing you have to supply is an appropriate
SQL query that transforms your data fromthe old schema into your model
structure. Dependencies between these migrations will be resolved
automatically. Give it a try!

This extension is tested automatically against:

* Django 1.5
* Django 1.6

on Python 2.7 and 3.3.

## Status of project

This app got extracted out of a production system and it requires some work in
creating tests, documentation and refactoring until it can be used by
everybody. Please be patient.

## Start participating

* Fork the project on Github and clone it locally
* Install Python 2.7 and 3.3, `virtualenv` and `tox`
* Run the tests with `tox` against all supported versions of Python
* Create a Pull Request on Github
