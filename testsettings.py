DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'data_migration',
    'data_migration.test_apps.blog',
)


SECRET_KEY = 'abcde12345'
