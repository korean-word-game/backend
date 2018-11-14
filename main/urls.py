from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('add_db/', views.word_plus)
]
