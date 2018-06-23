from django.shortcuts import render
from django.http import HttpResponse
from GamePlay.models import *

def GoNoGoRQ(request):
    if request.method == 'POST':
        username = request.POST['userName']
        stage = request.POST['stage']
        number = request.POST['gonogoNumber']
        oe = request.POST['omission_Error']
        ce = request.POST['comission_Error']
        success = request.POST['success']
        rt = request.POST['reactionTime']
        gonogo = GoNoGo()
        gonogo.userName = username
        gonogo.stage = stage
        gonogo.gonogoNumber = number
        gonogo.omission_Error = oe
        gonogo.comission_Error = ce
        gonogo.success = success
        gonogo.reactionTime = rt
        gonogo.save()
        return HttpResponse("gonogoSuccess")

    else:
        return HttpResponse("Post Error: GonoGo")

def NBackRQ(request):
    if request.method == 'POST':
        username = request.POST['userName']
        stage = request.POST['stage']
        nbackStage = request.POST['nbackStage']
        ac = request.POST['accuracy']
        rt = request.POST['reactionTime']
        nback = NBack()
        nback.userName = username
        nback.stage = stage
        nback.nbackStage = nbackStage
        nback.accuracy = ac
        nback.reactionTime = rt
        nback.save()
        return HttpResponse("NBackSuccess")

    else:
        return HttpResponse("Post Error: NBack")

def StroopRQ(request):
    if request.method == 'POST':
        username = request.POST['userName']
        stage = request.POST['stage']
        stStage = request.POST['stroopStage']
        accuracy = request.POST['accuracy']
        rt = request.POST['reactionTime']
        stroop = Stroop()
        stroop.userName = username
        stroop.stage = stage
        stroop.stroopStage = stStage
        stroop.accuracy = accuracy
        stroop.reactionTime = rt
        stroop.save()
        return HttpResponse("StroopSuccess")
    else:
        return HttpResponse("Post Error:Stroop")

def CardSortingRQ(request):
    if request.method == 'POST':
        username = request.POST['userName']
        stage = request.POST['stage']
        cardstate = request.POST['cardState']
        accuracy = request.POST['accuracy']
        rt = request.POST['reactionTime']
        cardsort = CardSorting()
        cardsort.userName = username
        cardsort.stage = stage
        cardsort.cardState = cardstate
        cardsort.accuracy = accuracy
        cardsort.reactionTime = rt
        cardsort.save()
        return HttpResponse("CardSortingSuccess")

    else:
        return HttpResponse("Post Error:CardSorting")

def MissionSatisfactionRQ(request):
    if request.methos == 'POST':
        username = request.POST['userName']
        mission = request.POST['mission']
        understood = request.POST['underStood']
        concentrate = request.POST['concentration']
        satisfy = request.POST['satisfaction']
        ms = MissionSatisfaction()
        ms.userName = username
        ms.mission = mission
        ms.underStood = understood
        ms.concentration = concentrate
        ms.satisfaction = satisfy
        ms.save()
        return HttpResponse("MissionSatisfactionSuccess")

    else:
        return HttpResponse("Post Error:MissionSatisfaction")
