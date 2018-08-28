from django.db import models
from django.contrib.auth.models import User

"""
# The game player (User)
class User(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.CharField(max_length=100, unique=True, null=False, blank=False)
    pw = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + ' / ' + str(self.date)
"""

# Additional information of a user
class AdditionalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

# Gonogo Game
class GonogoScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / accuracy:' + str(self.score) + ' / average_response_time:' + str(self.rt)

class GonogoStimulus(models.Model):
    gs = models.ForeignKey(GonogoScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.gs.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_date)

# CardsortScore Game
class CardsortScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / accuracy:' + str(self.score) + ' / average_response_time:' + str(self.rt)

class CardsortStimulus(models.Model):
    cs = models.ForeignKey(CardsortScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.cs.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_date)

# DigitNback Game
class DigitNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / accuracy:' + str(self.score) + ' / average_response_time:' + str(self.rt)

class DigitNbackStimulus(models.Model):
    ds = models.ForeignKey(DigitNbackScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.ds.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_date)

# ImageNback Game
class ImageNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / accuracy:' + str(self.score) + ' / average_response_time:' + str(self.rt)

class ImageNbackStimulus(models.Model):
    ims = models.ForeignKey(ImageNbackScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.ims.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_date)

# Tetris Game
class TetrisScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / ' + str(self.score)

# Stroop Game
class StroopScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / accuracy:' + str(self.score) + ' / average_response_time:' + str(self.rt)

class StroopStimulus(models.Model):
    ss = models.ForeignKey(StroopScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.ss.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_date)

# Balloon Game
class BalloonScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / average_response_time:' + str(self.rt)

class Balloon(models.Model):
    bs = models.ForeignKey(BalloonScore, on_delete=models.CASCADE)
    txt = models.CharField(max_length=50, null=False, blank=False)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    response = models.IntegerField(default=0)
    def __str__(self):
        return self.bs.user.name + ' / response_time:' + str(self.rt) + ' / ' + str(self.txt)

class BalloonText(models.Model):
    txt = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return self.txt

# Stroop Game
class Stroop2Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' / ' + str(self.score) + ' / ' + str(self.rt)

class Stroop2Stimulus(models.Model):
    s2s = models.ForeignKey(Stroop2Score, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.s2s.user.name + ' / ' + str(self.rt) + ' / ' + str(self.end_date)

