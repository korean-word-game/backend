from django.contrib import admin
from django.urls import path, re_path
from . import views

from django.conf.urls import url, include


urlpatterns = [
    path('signup', views.Register.as_view(), name='signup'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
