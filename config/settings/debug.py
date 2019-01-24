from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

WSGI_APPLICATION = '{PROJECT_NAME}.wsgi.debug.application'.format(PROJECT_NAME=PROJECT_NAME)

ROOT_URLCONF = '{PROJECT_NAME}.urls.debug'.format(PROJECT_NAME=PROJECT_NAME)

DATABASES = config_secret_common['django']['database'][0]
