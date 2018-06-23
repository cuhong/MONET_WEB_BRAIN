from django.db import models

class GoNoGo(models.Model):
    userName = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    gonogoNumber = models.CharField(max_length=50)
    omission_Error = models.CharField(max_length=50)
    comission_Error = models.CharField(max_length=50)
    success = models.CharField(max_length=50)
    reactionTime = models.CharField(max_length=50)

class NBack(models.Model):
    userName = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    nbackStage = models.CharField(max_length=50)
    nbackNum = models.CharField(max_length=50)
    accuracy = models.CharField(max_length=50)
    reactionTime = models.CharField(max_length=50)

class Stroop(models.Model):
    userName = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    stroopStage = models.CharField(max_length=50)
    # stroopNum = models.CharField(max_length=50)
    accuracy = models.CharField(max_length=50)
    reactionTime = models.CharField(max_length=50)

class CardSorting(models.Model):
    userName = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    cardNum = models.CharField(max_length=50)
    cardState = models.CharField(max_length=50)
    accuracy = models.CharField(max_length=50)
    reactionTime = models.CharField(max_length=50)

class MissionSatisfaction(models.Model):
    userName = models.CharField(max_length=50)
    mission = models.CharField(max_length=50)
    underStood = models.CharField(max_length=50)
    concentration = models.CharField(max_length=50)
    satisfaction = models.CharField(max_length=50)
