from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'itda', # DB명
        'USER': 'root', # 데이터베이스 계정
        'PASSWORD': 'dmzteamitda', # 계정 비밀번호
        'HOST': '52.79.234.92', # 데이테베이스 주소(IP)
        'PORT': '3306', # 데이터베이스 포트(보통은 3306)
    }
}

# WSGI application
WSGI_APPLICATION = 'koreanwordgame.wsgi.debug.application'

ROOT_URLCONF = 'koreanwordgame.urls.debug'
