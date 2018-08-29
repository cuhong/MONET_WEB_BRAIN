from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
import numpy as np

import os, sys
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import random

sys.path.insert(0, os.path.join(settings.BASE_DIR, 'ML/face_classification/src'))

from image_emotion_gender_demo import feed_forward

#from face_classsification.src.image_emotion_gender_demo import feed
#from .face_classification import src.image_emotion_gender_demo as model

# Create your views here.
def video(request):
    if request.method == "POST" or request.method == "OPTIONS":
        received_image = request.FILES['webcam']

        # Save the image to /uploads/
        path = default_storage.save(os.path.join(settings.MEDIA_ROOT, 'video/sample_image.jpg'), ContentFile(received_image.read()))  # 240 x 320 jpg file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # Find emotions list (if many people)
        try:
            emotion_list = feed_forward(os.path.join(settings.MEDIA_ROOT, 'video/sample_image.jpg'))
        except:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'video/sample_image.jpg'))
            return HttpResponse("오류가 발생했습니다. 다시 시도해 주세요.")

        if not emotion_list:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'video/sample_image.jpg'))
            return HttpResponse("얼굴이 너무 멀리 있어요!")

        # Remove created images
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video/sample_image.jpg'))
        os.remove(os.path.join(settings.MEDIA_ROOT, 'video/predicted_test_image.png'))

        # Return the emotion text (Ajax)
        return HttpResponse("당신의 감정은... {}".format(emotion_list[0]))
    return render(request, 'ML/video.html')

def audio(request):
    if request.method == "POST":
        #received_image = request.FILES['']
        print(request.body)

        # Save the audio to /uploads/audios/
        print("Received!")
        with open(os.path.join(settings.MEDIA_ROOT, 'audio/sample_audio.ogg'), 'wb') as f:
            f.write(request.body)

        # Deeplarning
        emotions = ['sad', 'happy', 'ignorant', 'interested']
        random.shuffle(emotions)

        # return message
        return HttpResponse("You look {}...".format(emotions[0]))

    return render(request, 'ML/audio.html')