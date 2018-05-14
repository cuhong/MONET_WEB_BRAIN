from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('which-game/', views.which_game, name='which_game'),
    path('game/<slug:game_name>/', views.game, name='game'),
    path('game/<slug:game_name>/game-result/', views.game_result, name='game_result'),
    path('logout/', views.logout, name='logout'),
]
