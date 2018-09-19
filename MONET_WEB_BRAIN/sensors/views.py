from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
def gyro(request):
    print(request.body)
    return HttpResponse("GOOD")