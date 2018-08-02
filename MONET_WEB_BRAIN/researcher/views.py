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
from django.conf import settings


import shutil
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
    if 'res_name' in request.session:
        return HttpResponseRedirect(reverse('researcher:upload', args=(request.session['res_name'], )))
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
            os.mkdir(os.path.join(settings.MEDIA_ROOT, researcher_name))
            os.mkdir(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/' + researcher_name))
            
            # Redirect the user to game upload webpage
            if 'prev' in request.session:
                return redirect(request.session['prev'])
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
                if 'prev' in request.session:
                    return redirect(request.session['prev'])
                return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name, )))
            return HttpResponseRedirect(reverse('researcher:sign_in'))
        else:
            return HttpResponseRedirect(reverse('researcher:sign_in'))
    else:
        form = SigninForm()
        return render(request, 'researcher/sign-in.html', {'form':form})

def projects(request, researcher_name):
    if 'res_name' not in request.session:
        request.session['prev'] = request.path
        return HttpResponseRedirect(reverse('researcher:sign_in'))

    """
    if request.method == 'POST':
        return render(request, 'researcher/{}/{}.html'.format(researcher_name, request.POST['game_name']))
    """

    this_researcher = get_object_or_404(Researcher, name=researcher_name)
    projects = ResearcherPrj.objects.filter(researcher=this_researcher)
    return render(request, 'researcher/projects.html', {'projects':projects, 'researcher_name':researcher_name})

def experiments(request, researcher_name, prj_name):
    """
    if 'res_name' not in request.session:
        request.session['prev'] = request.path
        return HttpResponseRedirect(reverse('researcher:sign_in'))
    """
    
    this_researcher = get_object_or_404(Researcher, name=researcher_name)
    this_prj = get_object_or_404(ResearcherPrj, researcher=this_researcher, prj_name=prj_name)
    experiments = ResearcherExp.objects.filter(prj=this_prj)
    return render(request, 'researcher/experiments.html', {'experiments':experiments, 'researcher_name':researcher_name, 'prj_name':prj_name})

def experiment(request, researcher_name, prj_name, exp_name):
    if request.method == 'POST':
        if 'res_name' not in request.session:
            request.session['prev'] = request.path
            return HttpResponseRedirect(reverse('researcher:sign_in'))    
        # No response default value
        base_response_time = 3000.0

        # Read the data sent by User in HttpRequest and parse it
        data = request.body.decode('utf-8')
        data_list = data.split('!')

        # Make a new data instance of this game's score
        new_score = ResearcherExpScore()
        this_resaercher = get_object_or_404(Researcher, name=resaercher_name)
        this_prj = get_object_or_404(ResearcherPrj, resaercher=this_resaercher, prj_name=prj_name)
        new_score.exp = get_object_or_404(ResearcherExp, prj=this_prj, exp_name=exp_name)
        #new_score.User = get_object_or_404(User, name=this_user_name)
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

    if 'name' not in request.session:
        request.session['prev'] = request.path
        return redirect('/game/sign_up/')
    return render(request, 'researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))

def remove_prj_dir(researcher_name, prj_name):
    # Remove the prject directory /uploads/{{researcher_name}}/{{prj_name}}/
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, '{}/{}/'.format(researcher_name, prj_name)))
    # Remove the game's html file at /researcher/templates/researcher/researchers/{{researcher_name}}/{{prj_name}}
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/'.format(researcher_name, prj_name)))
    except:
        print("html not created")
    
def delete_prj(request, researcher_name, prj_name):
        
    # Remove the physical directories of our server
    remove_prj_dir(researcher_name, game_name)

    # Delete the record of this prj from DB (the exps in this prj remove automatically by cascade)
    removed_prj = get_object_or_404(ResearcherPrj, prj_name=prj_name, researcher=get_object_or_404(Researcher, name=researcher_name))
    removed_prj.delete()

    return HttpResponseRedirect(reverse('researcher:index', args=(researcher_name,)))


# Game Upload pre- & post-processing
def upload(request, researcher_name):
    def txt_preprocessing(exp_file, exp_dir):
        """
        Change the path of text_file from relative path to absolute path
        """
        fsrc = codecs.open(exp_file, 'r', 'utf-8')
        lines = fsrc.readlines()
        fdest = open(exp_file, 'w', encoding='utf-8')
        for line in lines:
            #line = line.replace(replace, path+'/'+replace)
            if "text_file" in line:
                line_list = line.split(' ')
                line_list[2] = exp_dir + '/' + line_list[2]
                line = ' '.join(line_list)
            fdest.write(line)

    def html_postprocessing(html_file, researcher_name, prj_name, exp_name):
        """
        Change the path from relative to absolute so that can be found by apache2 server.
        """
        def img_parse(line, researcher_name, prj_name, exp_name):
            line = line.replace("img/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/img/')
            return line

        def audio_parse(line, researcher_name, prj_name, exp_name):
            line = line.replace("audio/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/audio/')
            return line

        def video_parse(line, researcher_name, prj_name, exp_name):
            line = line.replace("video/", "/upload_files/" + researcher_name + '/' + prj_name + '/' + exp_name + '/video/')
            return line

        def jspsych_parse(line):
            line = line.replace("jspsych.js", "{% static 'game/scripts/jspsych.js")  # {% static 'game/scripts/jspsych.js' %} => /static/game/scripts/jspsych.js
            line = line.replace("jspsych-6", "{% static 'game/jspsych-6")
            line = line.replace(".js\">", ".js' %}\">")
            line = line.replace("jspsych.css", "{% static 'game/styles/jspsych.css' %}")
            return line

        def send_result(line, researcher_name, prj_name, exp_name):
            line = line.replace("/* yumin accuracy */", "\
                accuracy = accuracy.toString();\n\
                start_time_list = start_time_list.toString();\n\
                end_time_list = end_time_list.toString();\n\
                response_time_list = rt.toString();\n\
                var xhr = new XMLHttpRequest();\n\
                xhr.open('POST', '/researcher/" + researcher_name +  "/" + prj_name + "/" + exp_name + "/', true);\n\
                xhr.setRequestHeader('Content-type', 'application/json');\n\
                xhr.onreadystatechange = function () {\n\
                    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
                    }\n\
                };\n\
                xhr.send(accuracy + '!' + response_time_list + '!' + start_time_list + '!' + end_time_list);\n\
                setTimeout(function () { window.location.replace('/researcher/" + researcher_name + "/" + prj_name + "/'); }, 1000);\n")

            line = line.replace("/* yumin no accuracy */", "\
                start_time_list = start_time_list.toString();\n\
                end_time_list = end_time_list.toString();\n\
                response_time_list = rt.toString();\n\
                var xhr = new XMLHttpRequest();\n\
                xhr.open('POST', '/researcher/" + researcher_name +  "/" + prj_name + "/" + exp_name + "/', true);\n\
                xhr.setRequestHeader('Content-type', 'application/json');\n\
                xhr.onreadystatechange = function () {\n\
                    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {\n\
                    }\n\
                };\n\
                xhr.send(response_time_list + '!' + start_time_list + '!' + end_time_list);\n\
                setTimeout(function () { window.location.replace('/researcher/" + researcher_name + "/" + prj_name + "/'); }, 1000);\n")
            return line

        f = codecs.open(html_file, 'r', 'utf-8')
        lines = f.readlines()
        fout = open(html_file, 'w', encoding='utf-8')

        i = 0
        for line in lines:
            if i == 0:
                line = line.replace(line, line+'{% load static %}\n')
                i += 1
            line = jspsych_parse(line)
            line = img_parse(line, researcher_name, prj_name, exp_name)
            line = audio_parse(line, researcher_name, prj_name, exp_name)
            line = video_parse(line, researcher_name, prj_name, exp_name)
            line = send_result(line, researcher_name, prj_name, exp_name)
            fout.write(line)

    def parse_descriptor(researcher_name, prj_name, prj_dir):
        exp_names = []
        
        with open(os.path.join(prj_dir, 'descriptor.txt'), 'r') as f:  # /uploads/{{researcher_name}}/{{prj_name}}/descriptor.txt
            print("Read descriptor.txt!")
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                # Read exp_name from descriptor.txt
                exp_name = str(row)
                exp_names.append(exp_name)
                exp_dir = os.path.join(prj_dir, exp_name)  # exp_dir = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}
                exp_file = os.path.join(exp_dir, 'exp.txt')  # exp_file = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}/exp.txt
                html_file = os.path.join(exp_dir, exp_name+'.html')  # html_file = /uploads/{{researcher_name}}/{{prj_name}}/{{exp_name}}/{{exp_name}}.html
                
                # Process the exp_file into html_file
                txt_preprocessing(exp_file, exp_dir)
                parser.generate_html(exp_file, html_file)
                html_postprocessing(html_file, researcher_name, prj_name, exp_name)

                # Copy result html_file into templates directory
                dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))
                shutil.copy2(html_file, dest)

        return exp_names

    def CreatePrj(fzip, researcher_name, prj_name, prj_dir):
        # prj_dir = /uploads/{{researcher_name}}/{{prj_name}}
        fzip_file = prj_dir + '/' + prj_name + '.zip'

        # Create zipfile into /uploads/{{researcher_name}}/{{prj_name}}/{{prj_name}}.zip
        with open(fzip_file, 'wb+') as destination:
            for chunk in fzip.chunks():
                destination.write(chunk)
        
        # Unzip zipfile into prj_dir
        import zipfile
        zip_ref = zipfile.ZipFile(fzip_file, 'r') 
        zip_ref.extractall(prj_dir)
        zip_ref.close()
        print("Successfully unzipped!")

        # Parse
        return parse_descriptor(researcher_name, prj_name, prj_dir)

        """
        # Preprocess 
        txt_preprocessing(path, "exp.txt")
        
        # Generate HTML file from parser
        parser.generate_html(path+'/exp.txt', path+'/'+gname+'.html')  # /uploads/ymkim_test3/djgame3/test_exp.txt

        # Move the created file from here to template directory
        source = path+'/'+gname+'.html'
        html_postprocessing(source, rname, gname)
        dest = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}.html'.format(rname, gname))
        shutil.copy2(source + '.tmp', dest)
        """


    if 'res_name' not in request.session:
        request.session['prev'] = request.path
        return HttpResponseRedirect(reverse('researcher:sign_up'))
    if request.method == 'POST':
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                prj_name = form.cleaned_data['title']
                print("The form is valid!")

                # If the form is valid, make the directory of this project
                prj_dir = os.path.join(settings.MEDIA_ROOT, '{}/{}'.format(researcher_name, prj_name))  # path = '/uploads/{{researcher_name}}/{prj_name}}'
                os.mkdir(prj_dir)

                # Create the project
                exp_names = CreatePrj(request.FILES['file'], researcher_name, prj_name, prj_dir)
                print("Project Created!")

                # Save this project's information into our DB
                new_prj = ResearcherPrj()
                new_prj.researcher = get_object_or_404(Researcher, name=researcher_name)
                new_prj.prj_name = prj_name
                new_prj.comment = form.cleaned_data['comment']
                new_prj.path = '/researcher/templates/researcher/researchers/{}/{}'.format(researcher_name, prj_name)
                os.mkdir(new_prj.path)  # Create the directory of this project in templates directory
                new_prj.save()

                for exp_name in exp_names:
                    new_exp = ResearcherExp()
                    new_exp.researcher = new_prj.researcher
                    new_exp.prj = new_prj
                    new_exp.exp_name = exp_name
                    new_exp.save()

        except:
            # If an error occurred, remove the game dirs
            print("ERROR occured while creating game")
            remove_prj_dir(researcher_name, form.cleaned_data['title'])

        return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name,)))
    else:
        form = UploadFileForm()
        return render(request, 'researcher/upload.html', {'form':form, 'researcher_name':researcher_name})


def logout(request):
    try:
        del request.session['res_name']
        del request.session['prev']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('researcher:sign_in'))

