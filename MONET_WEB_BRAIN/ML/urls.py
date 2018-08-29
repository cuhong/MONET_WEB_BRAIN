from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'ML'
urlpatterns = [
    path('video/', views.video, name='video'),
    path('audio/', views.audio, name='audio'),
]