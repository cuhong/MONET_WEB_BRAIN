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
    path('game/cardsort/cardsort_game.html', views.cardsort_game, name='cardsort_game'),
    path('game/stroop/stroop_game.html', views.stroop_game, name='stroop_game' ),
    path('game/stroop2/stroop2_game.html', views.stroop2_game, name='stroop2_game' ),
    path('researcher/sign-up/', views.researcher_sign_up, name='researcher_sign_up'),
    #path('researcher/sign-in/', views.researcher_sign_in, name='researcher_sign_in'),
]
