from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import *
import csv

def index(request):
    """
    Do: Redirect the user to the sign-up webpage. 
        If the user already logged-in, redirect him to the which-game webpage.
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
    Do: Show the sign-up webpage. If the user fill in the sign-up form,
    then let the user log-in automatically and redirect him to which-game
    webpage.
    """
    if request.method == 'GET':
        if 'name' in request.session:
            # User already logged-in
            return redirect('/which-game/')
    
        else:
            # Show the user the sign-up webpage
            return render(request, 'game/sign-up.html')
    
    elif request.method == 'POST':
        try:
            # Add new user to our database
            new_user = User()
            new_user.name = request.POST['name']
            new_user.email = request.POST['email']
            new_user.pw = request.POST['password']
            new_user.save()
        
        except IntegrityError as e: 
            # If there's already same name or email, reject the request
            if 'unique constraint' in e.message:
                raise Http404("You've already have an ID!")
        
        # From now, the user logged in.
        request.session['name'] = request.POST['name']

        # Redirect the user to game-selection webpage
        return redirect('/which-game/')

def sign_in(request):
    if request.method == 'GET':
        if 'name' in request.session:
            # User already logged-in
            return redirect('/which-game/')
        else:
            # Show the user the login webpage
            return render(request, 'game/sign-in.html')

    elif request.method == 'POST':
        # Read this user from the database. If failed, then return 404 error
        this_user = get_object_or_404(User, name=request.POST['name'])

        # If the typed password is eqaul to the user's password in DB,
        # then allow the login request
        if request.POST['password'] == this_user.pw:
            request.session['name'] = request.POST['name']
            return redirect('/which-game/')
    
        # Else, then redirect the user to sign-in webpage
        else:
            return redirect('/sign-in')

def which_game(request):
    """
    Do: Let the user select which game he will play, andr redirect him to the game
    """
    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return redirect('/')
        else:
            # show uer the game selection webpage
            return render(request, 'game/whichgame.html')

@csrf_exempt
def game(request, game_name):
    """
    Do: Let the user play the game whose index is 'game_index'
    Input: The game's index
    Output: The user's score.
    """
    # If the user is not logged in, redirect it to index webpage.
    if request.method == 'GET':
        if 'name' not in request.session:
            return redirect('/')
        else:
            # start the chosen game 
            if game_name == 'balloon':
                this_user = User.objects.get(name = request.session['name'])
                balloon_score = BalloonScore()
                balloon_score.user = this_user
                balloon_score.save()

                new_txt1 = BalloonText()
                new_txt1.bs = balloon_score
                new_txt1.txt = "MJPYEON is handsome."

                new_txt2 = BalloonText()
                new_txt2.bs = balloon_score
                new_txt2.txt = "HCAN is handsome."

                new_txt3 = BalloonText()
                new_txt3.bs = balloon_score
                new_txt3.txt = "HJCHA is handsome"

                new_txt1.save()
                new_txt2.save()
                new_txt3.save()
                balloon_txts = [new_txt1.txt, new_txt2.txt, new_txt3.txt]
                return render(request, 'game/' + game_name + '.html', {'balloon_txts' : balloon_txts})
            elif game_name == 'cardsort':
                with open('cardsorting_cond.csv', 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    all_lines = []
                    for row in reader:
                        all_lines.append('|'.join(row))
                    one_line = '@'.join(all_lines)
                    print(one_line)
                return render(request, 'game/' + game_name + '.html', {"csv_file": one_line})
            return render(request, 'game/' + game_name + '.html')
    elif request.method == 'POST':
        # Read the user's name from session and use it for querying
        this_user = User.objects.get(name = request.session['name']) 

        if game_name == 'gonogo':
            # Save the accuracy
            new_score = GonogoScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split(' ')
            new_score.score = float(json.loads(data_list[0]))
            new_score.rt = float(json.loads(data_list[1]))
            new_score.save()
        elif game_name == 'cardsort':
            # HAHA
            this_game = 'card_sort'
        elif game_name == 'digitnback':
             # Save the accuracy
            new_score = DigitNbackScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split(' ')
            new_score.score = float(json.loads(data_list[0]))
            new_score.rt = float(json.loads(data_list[1]))
            new_score.save()
        elif game_name == 'imagenback':
            new_score = ImageNbackScore()
            new_score.user = this_user
            data = request.body.decode('utf-8')
            data_list = data.split(' ')
            new_score.score = float(json.loads(data_list[0]))
            new_score.rt = float(json.loads(data_list[1]))
            new_score.save()
        elif game_name == 'tetris':
            # save the score
            new_score = TetrisScore()  # Make a new TetrisScore model instance
            new_score.user = this_user
            data = request.body.decode('utf-8')  # JSON data is in the body of the request, and since it was string let's decode it into 'utf-8' format.
            new_score.score = int(json.loads(data))
            new_score.save()
        elif game_name == 'balloon':
            this_bs = this_user.balloonscore_set.all().order_by('date').reverse()[0]
            this_txts = this_bs.balloontext_set.all().order_by('date')
            rt_array = request.body.decode('utf-8')
            rt_array_list = rt_array.split(',')
            print()
            print(rt_array_list)
            print()
            rt_array_list_fl = [ float(json.loads(i)) for i  in rt_array_list]
            for i, balloon_txt in enumerate(this_txts):
                balloon_txt.rt = rt_array_list_fl[i]
                balloon_txt.save()

        # After saving the usre's score, redirect the user to game-result webpage
        return redirect('/game/' + game_name + '/game-result/')
        

def game_result(request, game_name):
    """
    Do: Save the user's score in our database and then show the user the result comparing to other players.
    Input: The result of the user's game (score), and what the game the user played is.
    Output: In terms of the game he played, show the user's score and the Graph, Chart of the scores of the players.
    """
    # If the user is not logged in, redirect it to index webpage.
    if 'name' not in request.session:
        return redirect('/')

    # Save this user's user object as 'this_user'
    this_user = User.objects.get(name = request.session['name'])

    # Save this game's score object as 'this_game'    
    if game_name == 'gonogo':
        user_scores = GonogoScore.objects.filter(user=this_user).order_by('date').reverse()
        this_turn_score = user_scores[0]
        user_scores = user_scores[1:]

        all_scores = GonogoScore.objects.all().order_by('score').reverse()
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

        context = {'user_scores' : user_scores, 'all_scores' : all_scores, 'this_turn_score' : this_turn_score, 'user_rank' : user_rank, 'user_per' : user_per, 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)

    elif game_name == 'cardsort':
        this_game = CardsortScore
    elif game_name == 'digitnback':
        user_scores = DigitNbackScore.objects.filter(user=this_user).order_by('date').reverse()
        this_turn_score = user_scores[0]
        user_scores = user_scores[1:]

        all_scores = DigitNbackScore.objects.all().order_by('score').reverse()
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

        context = {'user_scores' : user_scores, 'all_scores' : all_scores, 'this_turn_score' : this_turn_score, 'user_rank' : user_rank, 'user_per' : user_per, 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'imagenback':
        user_scores = ImageNbackScore.objects.filter(user=this_user).order_by('date').reverse()
        this_turn_score = user_scores[0]
        user_scores = user_scores[1:]

        all_scores = ImageNbackScore.objects.all().order_by('score').reverse()
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

        context = {'user_scores' : user_scores, 'all_scores' : all_scores, 'this_turn_score' : this_turn_score, 'user_rank' : user_rank, 'user_per' : user_per, 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'tetris':
        # Read the user's all the scores of this game.
        user_scores = TetrisScore.objects.filter(user=this_user).order_by('date').reverse()
        # This turn's score should be the first item of date-orderd list
        this_turn_score = user_scores[0]
        # Except this turn's score from the list
        user_scores = user_scores[1:]
        # Read all the usre's all the scores of this game
        all_scores = TetrisScore.objects.all().order_by('score').reverse()
        # Calculate the user's ranking from all the users
        user_rank = 0
        for score in all_scores:
            user_rank += 1
            if score == this_turn_score:
                break

        all_scores_list = [str(i.score) for i in all_scores]
        all_scores_list_str = ','.join(all_scores_list)

        # Calcualte the percentage of this user.
        user_per = user_rank / len(all_scores) * 100

        user_per_str = str(user_per)[:4]
        user_per = float(user_per_str)
        context = {'user_scores' : user_scores, 'all_scores' : all_scores, 'this_turn_score' : this_turn_score, 'user_rank' : user_rank, 'user_per' : user_per, 'user_num' : len(all_scores), 'all_scores_list_str': all_scores_list_str}
        return render(request, 'game/game-result.html', context)
    elif game_name == 'balloon':
        return redirect('/')

def logout(request):
    try:
        del request.session['name']
    except KeyError:
        pass
    return redirect('/')

# Create your views here.
