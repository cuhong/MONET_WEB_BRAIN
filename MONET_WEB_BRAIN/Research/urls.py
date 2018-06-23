from django.urls import path
from .import views

app_name = 'Research'

urlpatterns =[
    path('MindState/', views.MindStateRQ),
    path('SelfEvaluation/', views.SelfValueRQ)
]