from django.contrib import admin
from django.urls import path, re_path
from . import views

from django.conf.urls import url, include


urlpatterns = [
    path('', views.wordgameMain.as_view(), name='wordgameMain'),
]
