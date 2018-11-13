from .base import *

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns.append(path('admin/', admin.site.urls))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)