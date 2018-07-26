from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.views import generic

import json
import csv
import dateutil.parser as dt
import os
import codecs
import parser

from .models import *
from .forms import *
#from .parser import *
from . import parser

def sign_up(request):
    if request.method == 'POST':
        # Read the form data in HttpRequest
        form = SignupForm(request.POST)

        if form.is_valid():
            researcher_name = form.cleaned_data['name']

            # If the form is valid, create & save new researcher into our database
            new_researcher = Researcher()
            new_researcher.name = researcher_name
            new_researcher.pw = form.cleaned_data['pw']
            new_researcher.email = form.cleaned_data['email']
            new_researcher.save()
            request.session['res_name'] = researcher_name

            # Create Researcher Directories
            from django.conf import settings
            os.mkdir(os.path.join(settings.MEDIA_ROOT, researcher_name))
            os.mkdir(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/' + researcher_name))
            
            # Redirect the user to game upload webpage
            return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name, )))

        return HttpResponseRedirect(reverse('researcher:sign_up'))
    else:
        form = SignupForm()
        return render(request, 'researcher/sign-up.html', {'form':form})

def sign_in(request):
    if request.method == 'POST':
        # Read the form data in HttpRequest
        form = SigninForm(request.POST)

        if form.is_valid():
            researcher_name = form.cleaned_data['name']
            this_researcher = get_object_or_404(Researcher, name=researcher_name)
            if form.cleaned_data['pw'] == this_researcher.pw:
                # Redirect the user to game upload webpage
                request.session['res_name'] = researcher_name
                return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name, )))
            return HttpResponseRedirect(reverse('researcher:sign_in'))
        else:
            return HttpResponseRedirect(reverse('researcher:sign_in'))
    else:
        form = SigninForm()
        return render(request, 'researcher/sign-in.html', {'form':form})

def index(request, researcher_name):
    if 'res_name' not in request.session:
        return HttpResponseRedirect(reverse('researcher:sign_in'))

    """
    if request.method == 'POST':
        return render(request, 'researcher/{}/{}.html'.format(researcher_name, request.POST['game_name']))
    """

    this_researcher = get_object_or_404(Researcher, name=researcher_name)
    games = ResearcherGame.objects.filter(researcher=this_researcher)
    return render(request, 'researcher/researcher.html', {'games':games, 'researcher_name':researcher_name})

def play_game(request, researcher_name, game_name):
    if request.method == 'POST':
        
        # No response default value
        base_response_time = 3000.0

        # Read the data sent by User in HttpRequest and parse it
        data = request.body.decode('utf-8')
        data_list = data.split('!')

        # Make a new data instance of this game's score
        new_score = ResearcherGameScore()
        new_score.game_name = game_name
        #new_score.User = get_object_or_404(User, name=this_user_name)
        new_score.researcher = get_object_or_404(Researcher, name=researcher_name)
        new_score.accuracy = float(json.loads(data_list[0]))  # accuracy
        sum = 0.0
        rt_list = data_list[1].split(',')  # response time list
        for rt in rt_list:
            try:
                sum += float(rt)
            except ValueError:
                sum += base_response_time
        if len(rt_list) != 0:
            new_score.avg_rt = sum/len(rt_list)
        new_score.save()

        # Parse start & end time list
        start_time_list = data_list[2].split(',')
        end_time_list = data_list[3].split(',')

        # Create and add each stimulus to our database.
        for i in range(len(rt_list)):
            new_stimulus = ResearcherGameStimulus()
            new_stimulus.rgs = new_score
            try:
                new_stimulus.rt = float(rt_list[i])
            except ValueError:
                new_stimulus.rt = base_response_time
            new_stimulus.start_time = dt.parse(start_time_list[i][:24])
            new_stimulus.end_time = dt.parse(end_time_list[i][:24])
            new_stimulus.save()

    if ('res_name' not in request.session) and ('name' not in request.session):
        return redirect('/researcher/sign-in/')
    return render(request, 'researcher/researchers/{}/{}.html'.format(researcher_name, game_name))

def txt_preprocessing(path, src):
    fsrc = codecs.open(path+'/'+src, 'r', 'utf-8')
    lines = fsrc.readlines()
    fdest = open(path+'/'+src, 'w', encoding='utf-8')
    for line in lines:
        #line = line.replace(replace, path+'/'+replace)
        if "text_file" in line:
            line_list = line.split(' ')
            line_list[2] = path + '/' + line_list[2]
            line = ' '.join(line_list)
        fdest.write(line)

def csv_to_template(html_fname, res_name, game_name):
    def img_parse(line, res_name, game_name):
        #line = line.replace("img src=\"img/", "img src=\"/uploads/" + res_name + '/' + game_name +'/img/')
        #line = line.replace("img src = ", "img src=' + ")
        line = line.replace("img/", "/upload_files/" + res_name + '/' + game_name + '/img/')
        return line

    def audio_parse(line, res_name, game_name):
        line = line.replace("audio/", "/upload_files/" + res_name + '/' + game_name + '/audio/')
        return line

    def video_parse(line, res_name, game_name):
        line = line.replace("video/", "/upload_files/" + res_name + '/' + game_name + '/video/')
        return line

    def jspsych_parse(line):
        line = line.replace("jspsych.js", "{% static 'game/scripts/jspsych.js")  # {% static 'game/scripts/jspsych.js' %} => /static/game/scripts/jspsych.js
        line = line.replace("jspsych-6", "{% static 'game/jspsych-6")
        line = line.replace(".js\">", ".js' %}\">")
        line = line.replace("jspsych.css", "{% static 'game/styles/jspsych.css' %}")
        return line

    f = codecs.open(html_fname, 'r', 'utf-8')
    lines = f.readlines()
    fout = open(html_fname + '.tmp', 'w', encoding='utf-8')

    i = 0
    for line in lines:
        if i == 0:
            line = line.replace(line, line+'{% load static %}\n')
            i += 1
        line = jspsych_parse(line)
        line = img_parse(line, res_name, game_name)
        line = audio_parse(line, res_name, game_name)
        line = video_parse(line, res_name, game_name)
        line = send_result(line, res_name, game_name)
        fout.write(line)

def html_postprocessing(html_path_name, res_name, game_name):
    #csv_to_template('Test_Experiment.html', 'ymkim', 'game1')
    csv_to_template(html_path_name, res_name, game_name)

def send_result(line, res_name, game_name):
    line = line.replace("/* yumin accuracy */", "\
        accuracy = accuracy.toString();\n\
        start_time_list = start_time_list.toString();\n\
        end_time_list = end_time_list.toString();\n\
        response_time_list = rt.toString();\n\
        var xhr = new XMLHttpRequest();\n\
        xhr.open('POST', '/researcher/" + res_name +  "/" + game_name + "/', true);\n\
        xhr.setRequestHeader('Content-type', 'application/json');\n\
        xhr.onreadystatechange = function () {\n\
            if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
            }\n\
        };\n\
        xhr.send(accuracy + '!' + response_time_list + '!' + start_time_list + '!' + end_time_list);\n\
        setTimeout(function () { window.location.replace('/researcher/" + res_name + "/'); }, 1000);\n")

    line = line.replace("/* yumin no accuracy */", "\
        start_time_list = start_time_list.toString();\n\
        end_time_list = end_time_list.toString();\n\
        response_time_list = rt.toString();\n\
        var xhr = new XMLHttpRequest();\n\
        xhr.open('POST', '/researcher/" + res_name +  "/" + game_name + "/', true);\n\
        xhr.setRequestHeader('Content-type', 'application/json');\n\
        xhr.onreadystatechange = function () {\n\
            if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
            }\n\
        };\n\
        xhr.send(response_time_list + '!' + start_time_list + '!' + end_time_list);\n\
        setTimeout(function () { window.location.replace('/researcher/"+ res_name + "/'); }, 1000);\n")
    return line

def CreateGame(fzip, rname, gname, path):
    # unzip to ./researchers/<researcher_name>/
    with open(path+'/'+gname+'.zip', 'wb+') as destination:
        for chunk in fzip.chunks():
            destination.write(chunk)
    import zipfile
    from django.conf import settings
    zip_ref = zipfile.ZipFile(path+'/'+gname+'.zip', 'r') 
    zip_ref.extractall(path)
    zip_ref.close()
    
    txt_preprocessing(path, "exp.txt")
    # Generate HTML file from parser
    parser.generate_html(path+'/exp.txt', path+'/'+gname+'.html')  # /uploads/ymkim_test3/djgame3/test_exp.txt

    # Move the created file from here to template directory
    source = path+'/'+gname+'.html'
    html_postprocessing(source, rname, gname)
    dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}.html'.format(rname, gname))
    import shutil
    shutil.copy2(source + '.tmp', dest)
    #os.rename(source, dest)

def remove_game_dir(rname, gname):
    import shutil
    print(rname, gname)
    # Remove the game directory /uploads/rname/gname/
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, '{}/{}/'.format(rname, gname)))
    # Remove the game's html file at /researcher/templates/researcher/researchers/rname/gname.html
    os.remove(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}.html'.format(rname, gname)))

def delete_game(request, researcher_name, game_name):
    remove_game_dir(researcher_name, game_name)
    # Delete the record of this game from DB
    removed_game = get_object_or_404(ResearcherGame, game_name=game_name, researcher=get_object_or_404(Researcher, name=researcher_name))
    removed_game.delete()
    return HttpResponseRedirect(reverse('researcher:index', args=(researcher_name,)))

def upload(request, researcher_name):
    if 'res_name' not in request.session:
        return HttpResponseRedirect(reverse('researcher:sign_up'))
    if request.method == 'POST':
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                game_title = form.cleaned_data['title']
                print("The form is valid!")
                from django.conf import settings

                # If the form is valid, make the directory of this game(experiment)
                path = os.path.join(settings.MEDIA_ROOT, '{}/{}'.format(researcher_name, game_title))  # path = '/uploads/researcher_name/game_title'
                os.mkdir(path)

                # Create the game
                CreateGame(request.FILES['file'], researcher_name, game_title, path)

                # Save this game's information into our DB
                new_game = ResearcherGame()
                new_game.researcher = get_object_or_404(Researcher, name=researcher_name)
                new_game.game_name = game_title
                new_game.comment = form.cleaned_data['comment']
                new_game.path = '/researcher/templates/researcher/{}/{}.html'.format(researcher_name, game_title)
                new_game.save()

        except:
            # If an error occurred, remove the game dirs
            print("ERROR occured while creating game")
            remove_game_dir(researcher_name, form.cleaned_data['title'])
        
        return HttpResponseRedirect(reverse('researcher:index', args=(researcher_name,)))
    else:
        form = UploadFileForm()
        return render(request, 'researcher/upload.html', {'form':form, 'researcher_name':researcher_name})

def logout(request):
    try:
        del request.session['res_name']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('researcher:sign_in'))

