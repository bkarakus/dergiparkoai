DEBUG = True

ALLOWED_HOSTS = ['*', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dergiparkoaidb',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': '983203',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}
