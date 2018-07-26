from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Researcher)
admin.site.register(ResearcherGame)
admin.site.register(ResearcherGameScore)
admin.site.register(ResearcherGameStimulus)