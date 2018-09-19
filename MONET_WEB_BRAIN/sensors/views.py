from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
import os

# Create your views here.
def gyro(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        with open(os.path.join(settings.BASE_DIR, 'sensors/gyro_log.txt'), 'a', encoding='utf-8') as f:
            f.write(data)
        return HttpResponse("GOOD")
    
    return render(request, 'sensors/test_sonsor.html')