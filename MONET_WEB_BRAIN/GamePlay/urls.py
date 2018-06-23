from django.urls import path
from .import views

app_name = 'GamePlay'

urlpatterns = [
    path('GoNoGo/', views.GoNoGoRQ),
    path('NBack/', views.NBackRQ),
    path('Stroop/', views.StroopRQ),
    path('CardSorting/', views.CardSortingRQ),
    path('MissionSatisfaction/', views.MissionSatisfactionRQ)

]