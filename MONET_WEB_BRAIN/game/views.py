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

"""
def ssl(request):
    f = open(os.path.join(settings.BASE_DIR, '1C7ACCC95D8133480DCF4A4EA241DD59.txt'), 'r')
    return HttpResponse(f, content_type='text/plain')
"""

def index(request):
    """
    Do: Redirect the user to the sign-up webpage.
        If the user already signed-in, redirect him to the which-game webpage.
    """
    if 'name' not in request.session:
        # User need to sign up or sign in
        ##return redirect('/sign-up/') --> Hard-coded version
        return HttpResponseRedirect(reverse('game:sign_up'))
    else:
        # Redirect the user to game selection webpage.
        return HttpResponseRedirect(reverse('game:which_game'))


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
            return HttpResponseRedirect(reverse('game:which_game'))
        else:
            # Show the user the sign-up webpage
            form = SignupForm()
            return render(request, 'game/sign-up.html', {'form':form})
    elif request.method == 'POST':
        try:
            # If the given form is valid & there's no error while querying, accept it.
            form = SignupForm(request.POST)
            if form.is_valid():
                # Add new user to our database
                new_user = User()
                new_user.name = form.cleaned_data['name']
                new_user.email = form.cleaned_data['email']
                new_user.pw = form.cleaned_data['pw']
                new_user.save()
                # From now, the user logged in.
                request.session['name'] = request.POST['name']
                # Redirect the user to game-selection webpage
                return HttpResponseRedirect(reverse('game:which_game'))
            else:
                # If the given form is invalid, raise 404 error
                raise Http404("It's not e-mail format!")
        except IntegrityError as e:
            # If there's already same name or email, reject the request
            if 'unique constraint' in e.message:
                raise Http404("You've already have an ID!")
            else:
                raise Http404("Database Integrity Error Occurred!")
    else:
        # We only support GET and POST methods, others are ignored by 404 error.
        return Http404('Invalid Request Method!\nOnly GET and POST are supported.')

def sign_in(request):
    """
    Do: [GET] Show the sign-in form. [POST] If the user's name is in
    User table and the password is correct, then redirect to which-game
    webpage and save the user's name in session. Otherwise, raise 404 error
    """
    if request.method == 'GET':
        if 'name' in request.session:
            # User already logged-in
            return HttpResponseRedirect(reverse('game:which_game'))
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
                # Validate the typed pw. If correct, redirect the user to game selection page.
                request.session['name'] = form.cleaned_data['name']
                return HttpResponseRedirect(reverse('game:which_game'))
            else:
                # If validation failed, redirect the user to sign-in webpage
                return HttpResponseRedirect(reverse('game:sign_in'))
        else:
            # If the form is invalid, then return 404
            return Http404('Invalid Form')
    else:
        # We only support GET and POST methods, others are ignored by 404 error.
        return Http404('Invalid Request Method!\nOnly GET and POST are supported.')
        

def which_game(request):
    """
    Do: Let the user select which game he will play, after that redirect him to the game
    """
    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return HttpResponseRedirect(reverse('game:index'))
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

    def calculate_avg_rt(rt_list, default_value):
        # Calculate average response time considering empty responses
        sum = 0.0
        for rt in rt_list:
            try:
                sum += float(rt)
            except ValueError:
                sum += default_value
        return sum / len(rt_list)
    
    def add_stimulus(StimulusClass, new_score, rt_list, start_date_list, end_date_list, default_value):
        # Save the result of each stimulus into database
        for i in range(len(rt_list)):
            new_stimulus = StimulusClass()
            new_stimulus.gs = new_score
            try:
                new_stimulus.rt = float(rt_list[i])
            except ValueError:
                new_stimulus.rt = default_value
            new_stimulus.start_date = dt.parse(start_date_list[i][:24])  # Remove redundant string after 24th index
            new_stimulus.end_date = dt.parse(end_date_list[i][:24])
            new_stimulus.save()

    def save_game_result(default_value, request, ScoreClass, StimulusClass, this_user):
        # Read the data sent by User in HttpRequest and parse it
        data = request.body.decode('utf-8')
        data_list = data.split('!')

        # Make a new data instance of this game's score
        new_score = ScoreClass()
        new_score.user = this_user
        new_score.score = float(json.loads(data_list[0]))
        rt_list = data_list[4].split(',')
        new_score.rt = calculate_avg_rt(rt_list, default_value)
        new_score.save()

        # Parse start & end time list
        start_date_list = data_list[2].split(',')
        end_date_list = data_list[3].split(',')

        # Create and add each stimulus to our database.
        add_stimulus(StimulusClass, new_score, rt_list, start_date_list, end_date_list, default_value)

    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return redirect('/')
        else:
            # start the chosen game
            if game_name == 'balloon':
                from random import shuffle
                # For the balloon game, we need to pre-read txts will be displayed in the balloons.
                this_user = User.objects.get(name=request.session['name'])
                questions = BalloonText.objects.all()
                questions = [question.txt for question in questions]
                shuffle(questions)
                # Pass the Question texts to the Web Client to display.
                balloon_txts = ','.join(questions)
                return render(request, 'game/{}.html'.format(game_name), {'balloon_txts': balloon_txts})
            else: 
                return render(request, 'game/{}.html'.format(game_name))

    elif request.method == 'POST':
        # Read the user's name from session and use it for querying
        this_user = User.objects.get(name=request.session['name'])

        if game_name == 'gonogo':
            # No response default value
            default_value = 1000.0

            # Read the data sent by User in HttpRequest and parse it
            data = request.body.decode('utf-8')
            data_list = data.split('!')

            # Make a new data instance of this game's score
            new_score = GonogoScore()
            new_score.user = this_user
            new_score.score = float(json.loads(data_list[0]))
            rt_list = data_list[4].split(',')
            new_score.rt = calculate_avg_rt(rt_list, default_value)
            new_score.save()

            # Parse start & end time list
            start_date_list = data_list[2].split(',')
            start_date_list = start_date_list[10:]  # Note that from 0 to 9th stimulus, test set.
            end_date_list = data_list[3].split(',')
            end_date_list = end_date_list[10:]

            # Create and add each stimulus to our database.
            add_stimulus(GonogoStimulus, new_score, rt_list, start_date_list, end_date_list, default_value)

        elif game_name == 'balloon':
            # Make a new data instance of this game's score
            balloon_score = BalloonScore()
            balloon_score.user = this_user
            balloon_score.save()

            # Read all the questions in the balloons from our database
            questions = BalloonText.objects.all()

            # Read the data sent by User in HttpRequest and parse it
            data = request.body.decode('utf-8')
            data_list = data.split('!')
            rt_list = data_list[0].split(',')
            st_list = data_list[1].split(',')
            et_list = data_list[2].split(',')
            responses_list = data_list[3].split(',')

            rt_list = [float(json.loads(i)) for i in rt_array_list]

            # Create and add balloons to our database.
            for i, question in enumerate(questions):
                balloon = Balloon()
                balloon.bs = balloon_score
                balloon.txt = question
                balloon.rt = rt_list[i]
                balloon.start_date = dt.parse(st_list[i][:24])
                balloon.end_date = dt.parse(et_list[i][:24])
                balloon.response = responses_list[i]
                balloon.save()

            balloon_score.rt = calculate_avg_rt(rt_list, 0.0)
            balloon_score.save()
    
        elif game_name == 'cardsort':
            save_game_result(1000.0, request, CardsortScore, CardsortStimulus, this_user)

        elif game_name == 'digitnback':
            save_game_result(2000.0, request, DigitNbackScore, DigitNbackStimulus, this_user)

        elif game_name == 'imagenback':
            save_game_result(2000.0, request, ImageNbackScore, ImageNbackStimulus, this_user)

        elif game_name == 'stroop':
            save_game_result(5000.0, request, StroopScore, StroopStimulus, this_user)

        elif game_name == 'stroop2':
            save_game_result(5000.0, request, Stroop2Score, Stroop2Stimulus, this_user)

        # After saving the usre's score, redirect the user to game-result webpage
        return redirect('/game/' + game_name + '/game-result/')


def game_result_context_maker(this_game_score, this_user):
    # Read recent 10 game scores of this user.
    user_scores = this_game_score.objects.filter(user=this_user).order_by('-date').reverse()
    #user_scores = this_game_score.objects.filter(user=this_user).order_by('date').reverse()
    this_turn_score = user_scores[0]
    user_scores = user_scores[1:]

    # Read all scores of this game
    all_scores = this_game_score.objects.all().order_by('-score').reverse()
    #all_scores = this_game_score.objects.all().order_by('score').reverse()

    # Calculate the ranking of this user of this game.
    user_rank = 0
    for score in all_scores:
        user_rank += 1
        if score == this_turn_score:
            break

    # Data to be delivered to the client(browser)
    all_scores_list = [str(i.score) for i in all_scores]
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
    'all_scores_list_str': all_scores_list_str }

    return context

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
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'cardsort':
        this_game_score = CardsortScore
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'digitnback':
        this_game_score = DigitNbackScore
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'imagenback':
        this_game_score = DigitNbackScore
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'tetris':
        this_game_score = TetrisScore
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'stroop':
        this_game_score = StroopScore
        context = game_result_context_maker(this_game_score, this_user)
        return render(request, 'game/game-result.html', context)

    elif game_name == 'stroop2':
        this_game_score = Stroop2Score
        context = game_result_context_maker(this_game_score, this_user)
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


