from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('db/', views.word_plus),
    path('', views.index, name='index'),
    path('game', views.game1, name='game'),
    path('api/makeroom/', views.make_room),
    path('api/playgame/', views.word_game),
    path('api/gamelog/', views.gamelog)
]
