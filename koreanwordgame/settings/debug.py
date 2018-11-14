from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']
os.path.join(CONFIG_SECRET_DIR, 'settings_debug.json')

DATABASES = config_secret_common['django']['database'][0]

WSGI_APPLICATION = 'koreanwordgame.wsgi.debug.application'

ROOT_URLCONF = 'koreanwordgame.urls.debug'
