from django.shortcuts import render
from django.http import HttpResponse
from Research.models import *

def MindStateRQ(request):
    if request.method == 'POST':
        username = request.POST['username']
        time = request.POST['time']
        anger = request.POST['anger']
        appearance = request.POST['appearance']
        mind = MindState()
        mind.username = username
        mind.time = time
        mind.anger = anger
        mind.appearance = appearance
        mind.save()
        return HttpResponse("MindStateSuccess")

    else:
        return HttpResponse("Post Error:MindState")

def SelfValueRQ(request):
    if request.method == 'POST':
        username = request.POST['username']
        selfval = request.POST['self_value']
        parval = request.POST['parent_value']
        frival = request.POST['friend_value']
        selfeval = SelfEvaluation()
        selfeval.username = username
        selfeval.self_value = selfval
        selfeval.parent_value = parval
        selfeval.friend_value = frival
        selfeval.save()
        return HttpResponse("SelfEvaluationSuccess")

    else:
        return HttpResponse("Post Error:SelfEvaluation")
