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
from django.contrib import messages

from django.contrib.auth.models import User

import shutil
import json
import csv
import dateutil.parser as dt
import os
import codecs

from .models import *
from .forms import UploadFileForm, SignupForm, SigninForm
#from .parser import *
from . import parser
from .parsing_utils import *

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
            os.mkdir(os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}'.format(researcher_name)))

            # Redirect the user to game upload webpage
            if 'prev' in request.session:
                return redirect(request.session['prev'])
            return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name, )))
        else:
            messages.success(request, '올바른 제출 양식이 아닙니다.')
            return HttpResponseRedirect(reverse('researcher:sign_up'))

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
            try:
                this_researcher = Researcher.objects.get(name=researcher_name)
            except:
                messages.success(request, '아이디가 존재하지 않습니다.')
                return HttpResponseRedirect(reverse('researcher:sign_in'))
            if form.cleaned_data['pw'] == this_researcher.pw:
                # Redirect the user to game upload webpage
                request.session['res_name'] = researcher_name
                if 'prev' in request.session:
                    return redirect(request.session['prev'])
                return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name, )))
            else:
                messages.success(request, '비밀번호가 틀렸습니다.')
                return HttpResponseRedirect(reverse('researcher:sign_in'))
        else:
            messages.success(request, '올바른 제출 양식이 아닙니다.')
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
    if 'name' not in request.session:
        request.session['prev'] = request.path
        return redirect('/game/sign_up/')

    this_user = get_object_or_404(User, username=request.session['name'])
    this_researcher = get_object_or_404(Researcher, name=researcher_name)
    this_prj = get_object_or_404(ResearcherPrj, researcher=this_researcher, prj_name=prj_name)
    experiments = ResearcherExp.objects.filter(prj=this_prj)

    # add booleans (T/F) denote that each project is done by this user.
    class exp:
        def __init__(self, experiment, user):
            scores = ResearcherExpScore.objects.filter(exp=experiment, user=user).order_by('-date')
            all_scores = ResearcherExpScore.objects.all()

            if len(scores) == 0:
                self.done = False
            else:
                self.done = True
                self.accuracy = scores[0].accuracy

                # Calculate the ranking of this user of this game.
                user_rank = 0
                for score in all_scores:
                    user_rank += 1
                    if score == self.accuracy:
                        break

            try:
                user_per = int(user_rank / len(all_scores) * 100)
            except:
                user_per = ''


            self.per = user_per

            self.experiment = experiment
            self.exp_name = experiment.exp_name.replace('_', ' ')

            
    experiments = [exp(experiment, this_user) for experiment in experiments]
    
    done = [exp.done for exp in experiments]
    done_true = [i for i in done if i]
    try:
        done_percent = int(len(done_true)/len(done)*100)
    except:
        done_percent = 0
        
    return render(request, 'researcher/experiments.html', {'done_percent': done_percent, 'done':done, 'project':this_prj, 'experiments':experiments, 'researcher_name':researcher_name, 'prj_name':prj_name})

def experiment(request, researcher_name, prj_name, exp_name):
    if request.method == 'POST':
        print('######################EXPERIMENT_RESULT_POST')
        if 'res_name' not in request.session:
            request.session['prev'] = request.path
            return HttpResponseRedirect(reverse('researcher:sign_in'))

        if exp_name.startswith('balloon'):
            # Ballon Experiment!
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            rt_list = data_list[0].split(',')
            start_time_list = data_list[1].split(',')
            end_time_list = data_list[2].split(',')
            responses_list = data_list[3].split(',')

            rt_list = [float(rt) for rt in rt_list]

            new_score = BalloonExpScore()

            this_researcher = get_object_or_404(Researcher, name=researcher_name)
            this_prj = get_object_or_404(ResearcherPrj, researcher=this_researcher, prj_name=prj_name)
            this_user = get_object_or_404(User, username=request.session['name'])

            new_score.exp = get_object_or_404(ResearcherExp, prj=this_prj, exp_name=exp_name)
            new_score.user = this_user
            new_score.save()

            # Read all the questions in the balloons from our database
            questions = []
            with open(os.path.join(settings.MEDIA_ROOT, '{}/{}/{}.txt'.format(researcher_name, prj_name, exp_name)), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    questions.append(line)

            for i, question in enumerate(questions):
                new_stimulus = BalloonExpStimulus()
                new_stimulus.bes = new_score
                new_stimulus.txt = question
                new_stimulus.rt = rt_list[i]
                new_stimulus.response = responses_list[i]
                new_stimulus.start_time = dt.parse(start_time_list[i][:24])
                new_stimulus.end_time = dt.parse(end_time_list[i][:24])
                new_stimulus.save()

        # No response default value
        base_response_time = 3000.0

        # Read the data sent by User in HttpRequest and parse it
        data = request.body.decode('utf-8')
        data_list = data.split('!')

        # Make a new data instance of this game's score
        new_score = ResearcherExpScore()
        this_researcher = get_object_or_404(Researcher, name=researcher_name)
        this_prj = get_object_or_404(ResearcherPrj, researcher=this_researcher, prj_name=prj_name)
        this_user = get_object_or_404(User, username=request.session['name'])
        new_score.exp = get_object_or_404(ResearcherExp, prj=this_prj, exp_name=exp_name)
        new_score.user = this_user
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

        # Parse start & end time list & responses
        start_time_list = data_list[2].split(',')
        end_time_list = data_list[3].split(',')
        response_list = data_list[4].split(',')

        # Create and add each stimulus to our database.
        for i in range(len(rt_list)):
            new_stimulus = ResearcherExpStimulus()
            new_stimulus.res = new_score
            try:
                new_stimulus.rt = float(rt_list[i])
            except ValueError:
                new_stimulus.rt = base_response_time
            new_stimulus.start_time = dt.parse(start_time_list[i][:24])
            new_stimulus.end_time = dt.parse(end_time_list[i][:24])
            new_stimulus.response = int(response_list[i])
            new_stimulus.save()
        return HttpResponse("Nice! This works")

    if 'name' not in request.session:
        request.session['prev'] = request.path
        return redirect('/game/sign_up/')
    return render(request, 'researcher/researchers/{}/{}/{}.html'.format(researcher_name, prj_name, exp_name))

def csv_download(request, researcher_name, prj_name, exp_name):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="some.csv"'

    writer = csv.writer(response)
    
    this_researcher = Researcher.objects.get(name=researcher_name)
    this_prj = ResearcherPrj.objects.get(researcher=this_researcher, prj_name=prj_name)
    this_exp = ResearcherExp.objects.get(prj=this_prj, exp_name=exp_name)

    scores = ResearcherExpScore.objects.filter(exp=this_exp).order_by('-date')

    for score in scores:
        writer.writerow([score.date, score.user.username, score.accuracy])

    return response

def delete_prj(request, researcher_name, prj_name):

    # Remove the physical directories of our server
    remove_prj_dir(researcher_name, prj_name)

    # Delete the record of this prj from DB (the exps in this prj remove automatically by cascade)
    removed_prj = get_object_or_404(ResearcherPrj, prj_name=prj_name, researcher=get_object_or_404(Researcher, name=researcher_name))
    removed_prj.delete()

    return HttpResponseRedirect(reverse('researcher:projects', args=(researcher_name,)))

# Game Upload pre- & post-processing
def upload(request, researcher_name):

    if 'res_name' not in request.session:
        request.session['prev'] = request.path
        return HttpResponseRedirect(reverse('researcher:sign_up'))
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        form.helper.form_action = reverse('researcher:upload', args=(researcher_name,))
        if form.is_valid():
            prj_name = form.cleaned_data['title']
            print("The form is valid!")

            # If the form is valid, make the directory of this project
            prj_dir = os.path.join(settings.MEDIA_ROOT, '{}/{}'.format(researcher_name, prj_name))  # path = '/uploads/{{researcher_name}}/{prj_name}}'
            prj_dir2 = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}'.format(researcher_name, prj_name))
            os.mkdir(prj_dir)
            os.mkdir(prj_dir2)

            # Create the project
            exp_names, exp_kor_names, exp_descriptions, exp_playtimes = CreatePrj(request.FILES['file'], researcher_name, prj_name, prj_dir)

            print("Project Created!")

            # Save this project's information into our DB
            new_prj = ResearcherPrj()
            new_prj.researcher = get_object_or_404(Researcher, name=researcher_name)
            new_prj.prj_name = prj_name
            new_prj.comment = form.cleaned_data['comment']
            new_prj.path = prj_dir2
            new_prj.save()

            for i, exp_name in enumerate(exp_names):
                new_exp = ResearcherExp()
                new_exp.researcher = new_prj.researcher
                new_exp.prj = new_prj
                new_exp.exp_name = exp_name
                new_exp.kor_exp_name = exp_kor_names[i]
                new_exp.description = exp_descriptions[i]
                new_exp.playtime = exp_playtimes[i]
                new_exp.save()
        messages.success(request, '성공적으로 프로젝트가 생성되었습니다.')
        return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name,)))

        """
        try:
            form = UploadFileForm(request.POST, request.FILES)
            form.helper.form_action = reverse('researcher:upload', args=(researcher_name,))
            if form.is_valid():
                prj_name = form.cleaned_data['title']
                print("The form is valid!")

                # If the form is valid, make the directory of this project
                prj_dir = os.path.join(settings.MEDIA_ROOT, '{}/{}'.format(researcher_name, prj_name))  # path = '/uploads/{{researcher_name}}/{prj_name}}'
                prj_dir2 = os.path.join(settings.BASE_DIR, 'researcher/templates/researcher/researchers/{}/{}'.format(researcher_name, prj_name))
                os.mkdir(prj_dir)
                os.mkdir(prj_dir2)

                # Create the project
                exp_names = CreatePrj(request.FILES['file'], researcher_name, prj_name, prj_dir)
                print("Project Created!")

                # Save this project's information into our DB
                new_prj = ResearcherPrj()
                new_prj.researcher = get_object_or_404(Researcher, name=researcher_name)
                new_prj.prj_name = prj_name
                new_prj.comment = form.cleaned_data['comment']
                new_prj.path = prj_dir2
                new_prj.save()

                for exp_name in exp_names:
                    new_exp = ResearcherExp()
                    new_exp.researcher = new_prj.researcher
                    new_exp.prj = new_prj
                    new_exp.exp_name = exp_name
                    new_exp.save()

        except:
            print("ERROR occured while creating project")
            remove_prj_dir(researcher_name, form.cleaned_data['title'])

        return HttpResponseRedirect(reverse('researcher:upload', args=(researcher_name,)))
        """
    else:
        form = UploadFileForm()
        return render(request, 'researcher/upload.html', {'form':form, 'researcher_name':researcher_name})

def result(request, researcher_name, prj_name, exp_name):
    this_researcher = Researcher.objects.get(name=researcher_name)
    this_user = User.objects.get(username=request.session['name'])
    this_prj = ResearcherPrj.objects.get(prj_name=prj_name, researcher=this_researcher)
    this_exp = ResearcherExp.objects.get(exp_name=exp_name, prj=this_prj)

    # Read recent 10 game scores of this user.
    user_scores = ResearcherExpScore.objects.filter(user=this_user, exp=this_exp).order_by('-date')
    #user_scores = this_game_score.objects.filter(user=this_user).order_by('date').reverse()
    this_turn_score = user_scores[0]
    user_scores = user_scores[1:]

    # Read all scores of this game
    all_scores = ResearcherExpScore.objects.filter(exp=this_exp).order_by('-accuracy')
    #all_scores = this_game_score.objects.all().order_by('score').reverse()

    # Calculate the ranking of this user of this game.
    user_rank = 0
    for score in all_scores:
        user_rank += 1
        if score == this_turn_score:
            break

    # Data to be delivered to the client(browser)
    all_scores_list = [str(i.accuracy) for i in all_scores]
    all_scores_list_str = ','.join(all_scores_list)

    user_per = user_rank / len(all_scores) * 100
    user_per_str = str(user_per)[:4]
    user_per = float(user_per_str)

    # Context to be delivered to the template renderer of django
    context = { 'user_scores': user_scores,
    'all_scores': all_scores,
    'this_turn_score': this_turn_score,
    'user_rank': user_rank,
    'user_per': user_per,
    'user_num': len(all_scores),
    'all_scores_list_str': all_scores_list_str,
    'researcher_name': researcher_name,
    'prj_name': prj_name,
     }

    return render(request, 'researcher/result.html', context)


def logout(request):
    try:
        del request.session['res_name']
        del request.session['prev']
        del request.session['name']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('researcher:sign_in'))

