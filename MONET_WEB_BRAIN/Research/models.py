from django.db import models

class MindState(models.Model):
    username = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    anger = models.CharField(max_length=50)
    attitude = models.CharField(max_length=50)
    appearance = models.CharField(max_length=50)

class SelfEvaluation(models.Model):
    username = models.CharField(max_length=50)
    self_value = models.CharField(max_length=50)
    parent_value =models.CharField(max_length=50)
    friend_value = models.CharField(max_length=50)
    