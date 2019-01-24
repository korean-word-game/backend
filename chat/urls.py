# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.Room.as_view(), name='room'),
]
