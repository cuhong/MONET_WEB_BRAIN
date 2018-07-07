from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import csv
import dateutil.parser as dt
import os
import codecs
import parser

from .models import *
from .forms import *
from .parser import *

def ssl(request):
    from django.conf import settings
    f = open(os.path.join(settings.BASE_DIR, '1C7ACCC95D8133480DCF4A4EA241DD59.txt'), 'r')
    return HttpResponse(f, content_type='text/plain')

def index(request):
    """
    Do: Redirect the user to the sign-up webpage.
        If the user already signed-in, redirect him to the which-game webpage.
    """
    if 'name' not in request.session:
        # User need to sign up or sign in
        return redirect('/sign-up/')
    else:
        # Redirect the user to game selection webpage.
        return redirect('/which-game/')


@csrf_exempt
def sign_up(request):
    """
    Do: [GET] Show the sign-up webpage. [POST] If the user fill-in the sign-up form,
    then save the user's data into User table in our database and let the user 
    log-in and redirect him to which-game webpage.
    """
    if request.method == 'GET':
        if 'name' in request.session:
            # User already logged-in
            return redirect('/which-game/')
        else:
            form = SignupForm()
            # Show the user the sign-up webpage
            return render(request, 'game/sign-up.html', {'form':form})
    elif request.method == 'POST':
        try:
            form = SignupForm(request.POST)
            if form.is_valid():
                # Add new user to our database
                new_user = User()
                new_user.name = form.cleaned_data['name']
                new_user.email = form.cleaned_data['email']
                new_user.pw = form.cleaned_data['pw']
                new_user.save()
            else:
                raise Http404("It's not e-mail format!")
        except IntegrityError as e:
            # If there's already same name or email, reject the request
            if 'unique constraint' in e.message:
                raise Http404("You've already have an ID!")
            else:
                raise Http404("Database Integrity Error Occurred!")
        # From now, the user logged in.
        request.session['name'] = request.POST['name']
        # Redirect the user to game-selection webpage
        return redirect('/which-game/')
    else:
        return Http404('Invalid Request Method!\nOnly GET and POST are supported.')

def sign_in(request):
    """
    Do: [GET] Show the sign-in form. [POST] If the user's name is in
    User table and the password is correct, then redirect to which-game
    webpage and save the user's name in session.
    """
    if request.method == 'GET':
        if 'name' in request.session:
            # User already logged-in
            return redirect('/which-game/')
        else:
            # Show the user the login webpage
            form = SigninForm()
            return render(request, 'game/sign-in.html', {'form':form})

    elif request.method == 'POST':
        # Read this user from the database. If failed, then return 404 error
        this_user = get_object_or_404(User, name=request.POST['name'])
        form = SigninForm(request.POST)
        if form.is_valid():
            # If the typed password is eqaul to the user's password in DB,
            # then allow the login request
            if form.cleaned_data['pw'] == this_user.pw:
                request.session['name'] = form.cleaned_data['name']
                return redirect('/which-game/')
            # Else, then redirect the user to sign-in webpage
            else:
                return redirect('/sign-in')
        else:
            return Http404('Invalid Request!')
    else:
        return Http404('Invalid Request Method!\nOnly GET and POST are supported.')
        

def which_game(request):
    """
    Do: Let the user select which game he will play, after that redirect him to the game
    """
    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return redirect('/')
        else:
            # show uer the game selection webpage
            return render(request, 'game/whichgame.html')
    else:
        return Http404('Invalid Request Method!\nOnly GET is supproted for this webpage.')


@csrf_exempt
def game(request, game_name):
    """
    Do: [GET] Let the user play the game whose index is 'game_index'
    [POST] Receive the user's score and game results then store them into database.
    After that redirect the user to the game-result webpage.
    """
    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return redirect('/')
        else:
            # start the chosen game
            if game_name == 'balloon':
                this_user = User.objects.get(name=request.session['name'])
                questions = BalloonText.objects.all()
                questions = [question.txt for question in questions]
                # Pass the Question texts to the Web Client to display.
                balloon_txts = ','.join(questions)
                return render(request, 'game/' + game_name + '.html', {'balloon_txts': balloon_txts})
            else: 
                return render(request, 'game/' + game_name + '.html')

    elif request.method == 'POST':
        # Read the user's name from session and use it for querying
        this_user = User.objects.get(name=request.session['name'])

        if game_name == 'gonogo':
            new_score = GonogoScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            # Calculate average response time considering empty responses
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 1000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()
            #start_date_list = data_list[2].split(',')
            #start_date_list = start_date_list[10:]
            #print('start_date_list', start_date_list)
            end_date_list = data_list[3].split(',')
            end_date_list = end_date_list[10:]
            # Save the result of each stimulus into database
            for i in range(len(rt_list)):
                new_stimulus = GonogoStimulus()
                new_stimulus.gs = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 1000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        elif game_name == 'cardsort':
            new_score = CardsortScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 1000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()

            #start_date_list = data_list[2].split(',')
            end_date_list = data_list[3].split(',')

            for i in range(len(rt_list)):
                new_stimulus = CardsortStimulus()
                new_stimulus.cs = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 1000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        elif game_name == 'digitnback':
            # Save the accuracy
            new_score = DigitNbackScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 2000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()

            #start_date_list = data_list[2].split(',')
            end_date_list = data_list[3].split(',')

            for i in range(len(rt_list)):
                new_stimulus = DigitNbackStimulus()
                new_stimulus.ds = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 2000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        elif game_name == 'imagenback':
            new_score = ImageNbackScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 2000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()

            #start_date_list = data_list[2].split(',')
            end_date_list = data_list[3].split(',')

            for i in range(len(rt_list)):
                new_stimulus = ImageNbackStimulus()
                new_stimulus.ims = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 2000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        elif game_name == 'tetris':
            # save the score
            new_score = TetrisScore()  # Make a new TetrisScore model instance
            new_score.user = this_user
            # JSON data is in the body of the request, and since it was string let's decode it into 'utf-8' format.
            data = request.body.decode('utf-8')
            new_score.score = int(json.loads(data))
            new_score.save()
        elif game_name == 'stroop':
            new_score = StroopScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 5000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()

            #start_date_list = data_list[2].split(',')
            end_date_list = data_list[3].split(',')

            for i in range(len(rt_list)):
                new_stimulus = StroopStimulus()
                new_stimulus.ss = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 5000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        elif game_name == 'balloon':
            balloon_score = BalloonScore()
            balloon_score.user = this_user
            balloon_score.save()

            questions = BalloonText.objects.all()
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            rt_array = data_list[0].split(',')
            st_list = data_list[1].split(',')
            et_list = data_list[2].split(',')
            responses = data_list[3].split(',')

            rt_array_list = rt_array
            rt_array_list_fl = [float(json.loads(i)) for i in rt_array_list]
            for i, question in enumerate(questions):
                balloon = Balloon()
                balloon.bs = balloon_score
                balloon.txt = question
                balloon.rt = rt_array_list_fl[i]
                balloon.start_date = dt.parse(st_list[i][:24])
                balloon.end_date = dt.parse(et_list[i][:24])
                balloon.response = responses[i]
                balloon.save()

            sum = 0.0
            for i in rt_array_list_fl:
                sum += i
            balloon_score.rt = sum / len(rt_array_list_fl)
            balloon_score.save()

        elif game_name == 'stroop2':
            new_score = Stroop2Score()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            new_score.score = float(json.loads(data_list[0]))
            sum = 0.0
            rt_list = data_list[4].split(',')
            for rt in rt_list:
                try:
                    sum += float(rt)
                except ValueError:
                    sum += 5000.0
            new_score.rt = sum/len(rt_list)
            new_score.save()

            #start_date_list = data_list[2].split(',')
            end_date_list = data_list[3].split(',')

            for i in range(len(rt_list)):
                new_stimulus = Stroop2Stimulus()
                new_stimulus.s2s = new_score
                try:
                    new_stimulus.rt = float(rt_list[i])
                except ValueError:
                    new_stimulus.rt = 5000.0
                #new_stimulus.start_date = dt.parse(start_date_list[i][:24])
                new_stimulus.end_date = dt.parse(end_date_list[i][:24])
                new_stimulus.save()
        # After saving the usre's score, redirect the user to game-result webpage
        return redirect('/game/' + game_name + '/game-result/')


def read_score(this_game_score, this_user):
    user_scores = this_game_score.objects.filter(user=this_user).order_by('date').reverse()
    this_turn_score = user_scores[0]
    user_scores = user_scores[1:]

    all_scores = this_game_score.objects.all().order_by('score').reverse()
    user_rank = 0
    for score in all_scores:
        user_rank += 1
        if score == this_turn_score:
            break

    all_scores_list = [str(i.score) for i in all_scores]
    all_scores_list_str = ','.join(all_scores_list)

    user_per = user_rank / len(all_scores) * 100
    user_per_str = str(user_per)[:4]
    user_per = float(user_per_str)
    return this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per


def game_result(request, game_name):
    """
    Do: Show the game result with ranking, graph.
    """
    # If the user is not logged in, redirect it to index webpage.
    if 'name' not in request.session:
        return redirect('/')

    # Save this user's user object as 'this_user'
    this_user = User.objects.get(name=request.session['name'])

    # Save this game's score object as 'this_game'
    if game_name == 'gonogo':
        this_game_score = GonogoScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'cardsort':
        this_game_score = CardsortScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'digitnback':
        this_game_score = DigitNbackScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'imagenback':
        this_game_score = DigitNbackScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'tetris':
        this_game_score = TetrisScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'stroop':
        this_game_score = StroopScore
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'stroop2':
        this_game_score = Stroop2Score
        this_turn_score, user_scores, all_scores, user_rank, all_scores_list_str, user_per = read_score(this_game_score, this_user)        
        context = {'user_scores': user_scores, 'all_scores': all_scores, 'this_turn_score': this_turn_score, 'user_rank': user_rank, 'user_per': user_per, 'user_num': len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'balloon':
        # Balloon game doesn't have any score.
        return redirect('/')

def logout(request):
    try:
        del request.session['name']
    except KeyError:
        pass
    return redirect('/')

def researcher_sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_researcher = Researcher()
            new_researcher.name = form.cleaned_data['name']
            new_researcher.pw = form.cleaned_data['pw']
            new_researcher.email = form.cleaned_data['email']
            new_researcher.save()
            request.session['res_name'] = form.cleaned_data['name']
            # Create Researcher Directories
            from django.conf import settings
            os.mkdir(os.path.join(settings.MEDIA_ROOT, form.cleaned_data['name']))
            os.mkdir(os.path.join(settings.BASE_DIR, 'game/templates/game/' + form.cleaned_data['name']))
            return redirect('/researcher/' + form.cleaned_data['name'] + '/upload/')
        return redirect('/researcher/sign-up/')
    else:
        form = SignupForm()
        return render(request, 'game/res-sign-up.html', {'form':form})

def researcher_sign_in(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            this_researcher = get_object_or_404(Researcher, name=form.cleaned_data['name'])
            if form.cleaned_data['pw'] == this_researcher.pw:
                request.session['res_name'] = form.cleaned_data['name']
                return redirect('/researcher/'+form.cleaned_data['name']+'/upload/')
            return redirect('/researcher/sign-in/')
        else:
            return redirect('/researcher/sign-in/')
    else:
        form = SigninForm()
        return render(request, 'game/res-sign-in.html', {'form':form})

def researcher(request, researcher_name):
    if 'res_name' not in request.session:
        return redirect('/researcher/sign-in/')
    if request.method == 'POST':
        path = 'game/' + request.session['res_name'] + '/'
        return render(request, path+request.POST['game_name']+'.html')
    this_researcher = get_object_or_404(Researcher, name=request.session['res_name'])
    games = ResearcherGame.objects.filter(researcher=this_researcher)
    return render(request, 'game/researcher.html', {'games':games, 'researcher_name':researcher_name})

def researcher_game(request, researcher_name, game_name):
    if ('res_name' not in request.session) and ('name' not in request.session):
        return redirect('/researcher/sign-in/')
    return render(request, 'game/' + researcher_name + '/' + game_name + '.html')

def txt_preprocessing(path, src, replace):
    fsrc = codecs.open(path+'/'+src, 'r', 'utf-8')
    lines = fsrc.readlines()
    fdest = open(path+'/'+src, 'w', encoding='utf-8')
    for line in lines:
        line = line.replace(replace, path+'/'+replace)
        fdest.write(line)

def html_postprocessing(html_path_name, res_name, game_name):
    #csv_to_template('Test_Experiment.html', 'ymkim', 'game1')
    csv_to_template(html_path_name, res_name, game_name)

def csv_to_template(html_fname, res_name, game_name):
    f = codecs.open(html_fname, 'r', 'utf-8')
    lines = f.readlines()
    fout = open(html_fname, 'w', encoding='utf-8')

    i = 0
    for line in lines:
        if i == 0:
            line = line.replace(line, line+'{% load static %}\n')
            i += 1
        line = jspsych_parse(line)
        line = img_parse(line, res_name, game_name)
        line = line.replace("jsPsych.data.get().localSave('csv', 'data.csv');", \
                "var trials = jsPsych.data.get().filter({test_part: 'test'});\n\
                var correct_trials = trials.filter({ correct: true});\n\
                var accuracy = Math.round(correct_trials.count() / trials.count() * 100);\n\
                var rt = trials.select('rt').values;\n\
                var avg_rt = trials.select('rt').mean();\n\
                var xhr = new XMLHttpRequest();\n\
                xhr.open('POST', '/game/" + res_name + '/' + game_name + "/', true);\n\
                xhr.setReqeustHeader('Content-type', 'application/json');\n\
                ");
        fout.write(line)

def img_parse(line, res_name, game_name):
    #line = line.replace("img src=\"img/", "img src=\"/uploads/" + res_name + '/' + game_name +'/img/')
    #line = line.replace("img src = ", "img src=' + ")
    line = line.replace("img/", "/upload_files/" + res_name + '/' + game_name + '/img/')
    return line

def jspsych_parse(line):
    line = line.replace("jspsych.js", "{% static 'game/scripts/jspsych.js")  # {% static 'game/scripts/jspsych.js' %} => /static/game/scripts/jspsych.js
    line = line.replace("jspsych-6", "{% static 'game/jspsych-6")
    line = line.replace(".js\">", ".js' %}\">")
    line = line.replace("jspsych.css", "{% static 'game/styles/jspsych.css' %}")
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
    
    txt_preprocessing(path, "test_exp.txt", "test_inst.txt")
    # Generate HTML file from parser
    generate_html(path+'/test_exp.txt', path)  # /uploads/ymkim_test3/djgame3/test_exp.txt
    # Move the created file from here to template directory
    source = path + '/Test_Experiment.html'
    html_postprocessing(source, rname, gname)
    dest = os.path.join(settings.BASE_DIR, 'game/templates/game/' + rname + '/' +  gname + '.html')
    os.rename(source, dest)

def upload(request, researcher_name):
    if 'res_name' not in request.session:
        return redirect('/researcher/sign-up/')
    researcher_name = request.session['res_name']
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("The form is valid!")
            from django.conf import settings
            path = os.path.join(settings.MEDIA_ROOT, researcher_name + '/' + form.cleaned_data['title'])
            os.mkdir(path)
            CreateGame(request.FILES['file'], researcher_name, form.cleaned_data['title'], path)
            new_game = ResearcherGame()
            new_game.researcher = get_object_or_404(Researcher, name=researcher_name)
            new_game.game_name = form.cleaned_data['title']
            new_game.path = '/game/templates/game/' + new_game.researcher.name + '/' + new_game.game_name + '.html'
            new_game.save()
        print("The form is invalid!")
        return redirect('/researcher/' + researcher_name + '/upload/')
    else:
        form = UploadFileForm()
        return render(request, 'game/upload.html', {'form':form, 'researcher_name':researcher_name})


