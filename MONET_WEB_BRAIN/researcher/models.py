from django.db import models

from django.contrib.auth.models import User

# The researcher
class Researcher(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.CharField(max_length=100, unique=True, null=False, blank=False)
    pw = models.CharField(max_length=30, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + ' / ' + str(self.date)

# The projects that belong to Resaercher
class ResearcherPrj(models.Model):
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    prj_name = models.CharField(max_length=20, null=False, blank=False)
    comment = models.TextField(max_length=200)
    path = models.CharField(max_length=150, null=False, blank=False)
    def __str__(self):
        return self.prj_name

# The experiments that belong to ResearcherPrj
class ResearcherExp(models.Model):
    prj = models.ForeignKey(ResearcherPrj, on_delete=models.CASCADE)
    exp_name = models.CharField(max_length=20, null=False, blank=False)
    description = models.CharField(max_length=200, default="New Experiment")
    playtime = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.exp_name

# Behavorial Experimental Game
class ResearcherExpScore(models.Model):
    exp = models.ForeignKey(ResearcherExp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accuracy = models.FloatField(default=-1.0)
    avg_rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + ' / accuracy:' + str(self.accuracy) + ' / average_response_time:' + str(self.avg_rt)

class ResearcherExpStimulus(models.Model):
    res = models.ForeignKey(ResearcherExpScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return self.res.user.username + ' / response_time:' + str(self.rt) + ' / ' + str(self.end_time)

class BalloonExpScore(models.Model):
    exp = models.ForeignKey(ResearcherExp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + self.date

class BalloonExpStimulus(models.Model):
    bes = models.ForeignKey(BalloonExpScore, on_delete=models.CASCADE)
    txt = models.CharField(max_length=100, null=False, blank=False)
    rt = models.FloatField(default=-1.0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    response = models.IntegerField(default=-1)
    def __str__(self):
        return '{} / response: {} / rt: {}'.format(self.bes.user.username, self.response, self.rt)
