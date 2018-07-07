from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'game'
urlpatterns = [
    path('.well-known/pki-validation/1C7ACCC95D8133480DCF4A4EA241DD59.txt/', views.ssl, name='ssl'),
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('which-game/', views.which_game, name='which_game'),
    path('game/<slug:game_name>/', views.game, name='game'),
    path('game/<slug:game_name>/game-result/', views.game_result, name='game_result'),
    path('logout/', views.logout, name='logout'),
    path('researcher/sign-up/', views.researcher_sign_up, name='researcher_sign_up'),
    path('researcher/sign-in/', views.researcher_sign_in, name='researcher_sign_in'),
    path('researcher/<slug:researcher_name>/', views.researcher, name='researcher'),
    path('researcher/<slug:researcher_name>/upload/', views.upload, name='upload'),
    path('researcher/<slug:researcher_name>/<slug:game_name>/', views.researcher_game, name = 'researcher_game'),
    path('researcher/<slug:researcher_name>/<slug:game_name>/delete/', views.delete_game, name='delete_game'),
    path('researcher/logout/', views.res_logout, name='res_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
