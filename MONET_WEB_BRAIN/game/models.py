from django.db import models

# The game player (User)
class User(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.CharField(max_length=100, unique=True, null=False, blank=False)
    pw = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

# Gonogo Game
class GonogoScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class GonogoStimulus(models.Model):
    gs = models.ForeignKey(GonogoScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

# CardsortScore Game
class CardsortScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class CardsortStimulus(models.Model):
    cs = models.ForeignKey(CardsortScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

# DigitNback Game
class DigitNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class DigitNbackStimulus(models.Model):
    ds = models.ForeignKey(DigitNbackScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)    

# ImageNback Game
class ImageNbackScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class ImageNbackStimulus(models.Model):
    ims = models.ForeignKey(DigitNbackScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)  

# Tetris Game
class TetrisScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score)

# Stroop Game
class StroopScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=-1.0)
    rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + ' ' + str(self.score) + ' ' + str(self.rt)

class StroopStimulus(models.Model):
    ss = models.ForeignKey(DigitNbackScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

# Balloon Game
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
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.bs.user.name + ' ' + str(self.txt) + ' ' + str(self.rt)

class BalloonText(models.Model):
    txt = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return self.txt
