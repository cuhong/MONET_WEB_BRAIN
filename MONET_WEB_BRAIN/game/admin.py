from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(GonogoScore)
admin.site.register(CardsortScore)
admin.site.register(DigitNbackScore)
admin.site.register(ImageNbackScore)
admin.site.register(TetrisScore)
admin.site.register(BalloonScore)
admin.site.register(BalloonText)
