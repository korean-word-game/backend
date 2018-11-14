from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

WSGI_APPLICATION = 'koreanwordgame.wsgi.deploy.application'

ROOT_URLCONF = 'koreanwordgame.urls.deploy'

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