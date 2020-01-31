from django.urls import path

from . import views

app_name = 'gameLibrary'

urlpatterns = [
    path('', views.home, name='home'),
    path('browseGames/', views.browseGames, name='browseGames'),
    path('myGames/', views.myGames, name='myGames'),
    path('playGame/<int:game_id>', views.playGame, name='playGame'),
    path('addGame/', views.addGame, name='addGame'),
    path('api/', views.api, name='api'),
]