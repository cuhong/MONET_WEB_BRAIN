from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Researcher)
admin.site.register(ResearcherPrj)
admin.site.register(ResearcherExp)
admin.site.register(ResearcherExpScore)