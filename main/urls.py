from django.urls import path

from . import views

urlpatterns = [
    path('db/', views.word_plus),
    path('', views.index, name='index'),
    path('game', views.game1, name='game'),
    path('api/makeroom/', views.make_room),
    path('api/playgame/', views.word_game)
]
