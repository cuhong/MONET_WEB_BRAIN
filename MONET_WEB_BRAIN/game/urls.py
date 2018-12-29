from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'game'
urlpatterns = [
    #path('.well-known/pki-validation/1C7ACCC95D8133480DCF4A4EA241DD59.txt/', views.ssl, name='ssl'),
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('which-game/', views.which_game, name='which_game'),
    path('game/<slug:game_name>/', views.game, name='game'),
    path('game/<slug:game_name>/game-result/', views.game_result, name='game_result'),
    path('logout/', views.logout, name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('teen_auth/<slug:user_name>/', views.teen_auth, name='teen_auth'),
    path('agreement/', views.user_agreement, name='user_agreement'),
    path('i_agree/', views.i_agree, name='i_agree'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
