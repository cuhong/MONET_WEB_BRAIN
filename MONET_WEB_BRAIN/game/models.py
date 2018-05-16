from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.CharField(max_length=100, unique=True, null=False, blank=False)
    pw = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class GonogoScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class CardsortScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class DigitNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class ImageNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class TetrisScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score)

class StroopScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)
        
class BalloonScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class Balloon(models.Model):
    bs = models.ForeignKey(BalloonScore, on_delete=models.CASCADE)
    txt = models.CharField(max_length=50, null=False, blank=False)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.bs.user.name + ' ' + str(self.txt) + ' ' + str(self.rt)

class BalloonText(models.Model):
    txt = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return self.txt

# Create your models here.
