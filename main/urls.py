from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('db/', views.word_plus),
    path('makeroom/', views.make_room),
    path('playgame/', views.word_game)
]
