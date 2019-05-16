from django.db import models
from datetime import datetime, timedelta

#Tournament class contains all the required fields needed to get questions from the API and it is also used to output details of the tournaments in the home page
class Tournament(models.Model):

    DIFFICULTY = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    )

    name = models.CharField(
        max_length=100,
        default='')

    start_date = models.DateField()

    end_date = models.DateField()

    category = models.CharField(
        max_length=200,
        default='Any Category')

    difficulty = models.CharField(
        max_length=100,
        choices=DIFFICULTY,
        default='Easy')

#The questions are all stores along with their correct answer and a foreign key value of the Tournament that it belongs to
class Question(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    correct_ans = models.CharField(max_length=200)

#Both correct and incorrect answers are stored here so that they can be displayed to the user in a mixed format each time
#And a foreign key value of the Question that it belongs to
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

#Stores the player, the tournament they've entered, the question they're currently on and their score for that tournament
class Player_Scores(models.Model):
    username = models.CharField(max_length=200)
    tournament = models.IntegerField()
    current_question = models.IntegerField()
    score = models.IntegerField()