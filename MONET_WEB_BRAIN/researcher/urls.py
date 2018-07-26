from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'researcher'
urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout, name='logout'),
    path('<slug:researcher_name>/', views.index, name='index'),
    path('<slug:researcher_name>/upload/', views.upload, name='upload'),
    path('<slug:researcher_name>/<slug:game_name>/', views.play_game, name = 'play_game'),
    path('<slug:researcher_name>/<slug:game_name>/delete/', views.delete_game, name='delete_game'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
