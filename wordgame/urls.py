from django.contrib import admin
from django.urls import path, re_path
from . import views

from django.conf.urls import url, include


urlpatterns = [
    path('', views.wordgameMain.as_view(), name='wordgameMain'),
    path('ingame', views.wordgameIngame.as_view(), name='wordgameIngame'),
    path('search/<mode>', views.wordgameSearch.as_view(), name='wordgameSearch'),
    path('makeroom', views.makeRoom.as_view(), name='makeRoom'),
]
