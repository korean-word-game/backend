from django.urls import path, include


urlpatterns = [
    path('', include('wordgame.urls')),
    path('account/', include('users.urls')),
]

