from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

WSGI_APPLICATION = '{PROJECT_NAME}.wsgi.deploy.application'.format(PROJECT_NAME=PROJECT_NAME)

ROOT_URLCONF = '{PROJECT_NAME}.urls.deploy'.format(PROJECT_NAME=PROJECT_NAME)

DATABASES = config_secret_common['django']['database'][0]