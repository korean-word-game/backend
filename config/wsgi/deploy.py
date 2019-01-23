import os

from django.core.wsgi import get_wsgi_application
from ..settings.base import PROJECT_NAME

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{PROJECT_NAME}.settings.deploy')

application = get_wsgi_application()