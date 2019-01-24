import os

from django.core.wsgi import get_wsgi_application
from ..settings.base import PROJECT_NAME

os.environ.setdefault("DJANGO_SETTINGS_MODULE", '{PROJECT_NAME}.settings.deploy'.format(PROJECT_NAME=PROJECT_NAME))

application = get_wsgi_application()