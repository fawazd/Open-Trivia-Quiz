from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, get_user_model, logout,)
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.contrib import messages
import requests


from .models import Tournament, Question, Answer, Player_Scores

categories = {}

class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        #Returns every tournament object in the database to the index page.
        current_date = datetime.date.today()
        active = Tournament.objects.filter(start_date__lte = current_date, end_date__gte = current_date)
        upcoming = Tournament.objects.filter(start_date__gt = current_date)

        return render(request,'polls/index.html', {'active':active, 'upcoming':upcoming})

super = user_passes_test(lambda u: u.is_superuser)
class CreateTournamentView(View):
    @method_decorator(super)
    def get(self, request):
        #Retrieves the categories from opentdb
        response = requests.get('https://opentdb.com/api_category.php')
        data = json.loads(response.content)
        #As the question url requires a number instead of text for the category,
        # I saw that Aidyn was having this issue when he was trying to get the questions,
        # so I came up with the idea of using a dictionary so that you can store both the ID and the name of the category.
        for cat in data['trivia_categories']:
            categories["%d" % cat["id"]] = cat['name']
        #Passing in the categories dictionary so that the creat tournament html can fill a dropdown with all the category names.
        return render(request,'polls/create_tourny.html', {'categories':categories})

    @method_decorator(super)
    def post(self, request):
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        difficulty = request.POST.get('difficulty').lower()
        category = request.POST.get('category')

        #At th same time I use the url provided by opentdb to grab 10 questions using the specified category and difficulty by the User.
        response = requests.get('https://opentdb.com/api.php?amount=10&category=%s&difficulty=%s' % (category, difficulty))
        data = json.loads(response.content)
        if data['response_code'] == 0:
            # Using the user's selections, I create the tournament object.
            tournament = Tournament.objects.create(name=name, start_date=start_date, end_date=end_date,
                                                   difficulty=difficulty, category=categories.get("%s" % category))
            tournament.save()
            for q in data['results']:
                #Looping through the json data, I create a question object for each question. Passing in the tournament object created earlier as the foreign key.
                #I also store the correct answer in the question object so that I may compare the user selected answer to it during the quiz.
                question = Question.objects.create(tournament = tournament, question_text = q["question"], correct_ans = q["correct_answer"])
                #Here I create an object for each incorrect answer and the correct answer, passing in the question created as the foreign key.
                answer = Answer.objects.create(question = question, answer_text = q["correct_answer"])
                answer.save()
                for ans in q["incorrect_answers"]:
                    answer = Answer.objects.create(question = question, answer_text = ans)
                    answer.save()
        #Once the tournament is created, the user is redirected to the homepage, which will display all the tournaments.
        current_date = datetime.date.today()
        active = Tournament.objects.filter(start_date__lte = current_date, end_date__gte = current_date)
        upcoming = Tournament.objects.filter(start_date__gt = current_date)
        return render(request, 'polls/index.html', {'active':active, 'upcoming':upcoming})

class LoginView(View):
    def get(self, request):
        return render(request, 'polls/login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/login.html')

class SignUpView(View):
    def get(self, request):
        return render(request, 'polls/signup.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != "" and password != "":
            user = User.objects.create_user(first_name = '', last_name = '', email = '', username=username, password=password)
            user.save()
            return HttpResponseRedirect(reverse('polls:login'))
        else:
            return render(request, 'polls/signup.html')

class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('polls:login'))

class TournamentView(View):
    @method_decorator(login_required)
    def get(self, request, tournament_id):
        #When a tournament is selected in the homepage, it leads to that url and passes in tournament id to the url.
        #The tournament id is then used here to run the questions and keep track of player scores for the specified tournament.
        current_tournament = Tournament.objects.get(id=tournament_id)
        #I check here if the user has already entered this tournament, if not, I create a new record for that in the database
        if Player_Scores.objects.filter(username = request.user.username, tournament = tournament_id).count() < 1:
            new_entry = Player_Scores.objects.create(username = request.user.username, tournament = tournament_id, current_question = 0, score = 0)
            new_entry.save()
        #Gets the instance of the object from play_scores for the currently logged in player and the entered tournament.
        current_user = Player_Scores.objects.get(username = request.user.username, tournament = tournament_id)

        #If the user hasn't already completed the quiz, aka reached 10 questions, then it runs the normal quiz code
        if current_user.current_question < 10:
            #Filters the questions for the selected tournament
            questions = Question.objects.filter(tournament=tournament_id).order_by('id')
            #Grabs the question based on the current question the user is on from the Player_Scores database
            question = questions[current_user.current_question]
            #Gets all answers for the selected question and mixes them up
            answers = Answer.objects.filter(question = question).order_by('?')

            #Sends all the required variables I've stored to the tournament html to display the quiz for the current question they're on
            return render(request, 'polls/tournament.html', {'tournament': current_tournament, 'question': question, "answers": answers, 'question_num': current_user.current_question + 1})
        else:
            #If they have already completed the quiz and answered 10 questions, they are then redirected to the results page where they can view their score for that quiz
            return HttpResponseRedirect(reverse('polls:results', kwargs={"score": current_user.score}))

    @method_decorator(login_required)
    def post(self, request):
        current_user = Player_Scores.objects.get(username=request.user.username, tournament = request.POST.get("tournament_id"))
        #Gets the lot of questions filtered by the the current tournament
        questions = Question.objects.filter(tournament=request.POST.get("tournament_id")).order_by('id')
        #Getting the current question so that I can check whether or not I the selected answer is correct.
        question = questions[current_user.current_question]
        question_num = str(current_user.current_question + 1)

        # Here I'm setting messages that can be display to the user, to give them feedback
        # I'm also incrementing their score if they got the question right
        if request.POST.get("answers") == question.correct_ans:
            current_user.score += 1
            messages.success(request, 'You got question %s: Correct!' % question_num)
        else:
            messages.error(request, 'You got question %s: Incorrect' % question_num)
        #Incrementing the current question so that the next question is displayed when it's re-directed
        current_user.current_question += 1
        current_user.save()

        return HttpResponseRedirect(reverse('polls:tournament', kwargs={"tournament_id": request.POST.get("tournament_id")}))

class HighscoresView(View):
    def get(self, request):
        high_scores = []
        #Gets all the scores in the player_scores table if they have a current_question value of 10 to make sure that the quiz was completed
        all_scores = Player_Scores.objects.filter(current_question = 10)
        #For each of the scores, I filter another set of the player scores using the tournament from each of the scores in the first list
        #I then order by the highest score and get the first value and store it, so even if 2 people have the same high score, the person who got the high score first is the one that is displayed
        for s in all_scores:
            filtered_scores = Player_Scores.objects.filter(tournament=s.tournament).order_by('-score')
            high_scores.append(filtered_scores[0])
        #Here I get rid of duplicates and send it over to the highscores html
        scores = list(set(high_scores)).order_by('tournament')
        tournaments = Tournament.objects.all()
        return render(request, 'polls/highscores.html', {"highscores": scores, "tournaments": tournaments})

class ResultsView(View):
    @method_decorator(login_required)
    def get(self, request, score):
        return render(request, 'polls/results.html', {"score": score})