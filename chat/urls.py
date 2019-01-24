# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.room.as_view(), name='room'),
]