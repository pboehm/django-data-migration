# -*- coding: utf-8 -*-
import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# import package version
with open('data_migration/version.py') as f:
    exec(f.read())

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-data-migration',
    version=__version__,
    packages=["data_migration", "data_migration.management.commands"],
    include_package_data=True,
    license='MIT License',
    description='Data migration framework for Django that migrates legacy data into your new django app',
    long_description=README,
    url='https://github.com/pboehm/django-data-migration',
    author='Philipp Böhm',
    author_email='dev@pboehm.org',
    install_requires=['networkx >= 1.8.0', 'future'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
