from django.db import models

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
        return self.game_name

# The experiments that belong to ResearcherPrj
class ResearcherExp(models.Model):
    prj = models.ForeignKey(ResearcherPrj, on_delete=models.CASCADE)
    exp_name = models.CharField(max_length=20, null=False, blank=False)
    def __str__(self):
        return self.exp_name

# Behavorial Experimental Game
class ResearcherExpScore(models.Model):
    exp = models.ForeignKey(ResearcherExp, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    accuracy = models.FloatField(default=-1.0)
    avg_rt = models.FloatField(default=-1.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ' / accuracy:' + str(self.accuracy) + ' / average_response_time:' + str(self.avg_rt)

class ResearcherExpStimulus(models.Model):
    rgs = models.ForeignKey(ResearcherExpScore, on_delete=models.CASCADE)
    rt = models.FloatField(default=-1.0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return ' / response_time:' + str(self.rt) + ' / ' + str(self.end_time)