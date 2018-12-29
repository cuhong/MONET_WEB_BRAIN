from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Researcher)
admin.site.register(ResearcherPrj)
admin.site.register(ResearcherExp)
#admin.site.register(ResearcherExpScore)
admin.site.register(ResearcherExpStimulus)
admin.site.register(BalloonExpScore)
admin.site.register(BalloonExpStimulus)

class ExpStimulus(admin.ModelAdmin):
    model = ResearcherExpStimulus
    list_display = ['rt', 'response', 'start_time', 'end_time', ]

admin.site.register(ResearcherExpScore, ExpStimulus)