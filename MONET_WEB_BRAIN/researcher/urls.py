from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'researcher'
urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout, name='logout'),
    path('<slug:researcher_name>/', views.projects, name='projects'), # Show the projects which belong to this researcher
    path('<slug:researcher_name>/upload/', views.upload, name='upload'),
    path('<slug:researcher_name>/<slug:prj_name>/', views.experiments, name = 'experiments'), # Show the experiments which belong to this project
    path('<slug:researcher_name>/<slug:prj_name>/<slug:exp_name>/', views.experiment, name='experiment'),
    path('<slug:researcher_name>/<slug:prj_name>/delete/', views.delete_prj, name='delete_prj'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
