from django.urls import path
from . import views

app_name = 'sensors'
urlpatterns = [
    path('gyro/', views.gyro, name='gyro'),

]