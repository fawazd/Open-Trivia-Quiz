from django.db.models.query import QuerySet
from django.test import TestCase

from .models import Tournament, Question, Answer, Player_Scores
from polls import views
from django.contrib.auth.models import User

class TestHomeView(TestCase):
    def setUp(self):
        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")
    #Checks if anon attempt to access a page and that it redirects them to the login
    def test_call_index_denies_anonymous(self):
        response = self.client.get('/polls/index/', follow=True)
        self.assertRedirects(response, '/polls/login/?next=/polls/index/')

#I'm checking that a super user is able to access the create page and create a tournment by testing the post as well.
class TestCreateView(TestCase):
    def setUp(self):
        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")

    def test_call_view_loads_create(self):
        self.client.login(username='super', password='pass')
        response = self.client.get('/polls/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/create_tourny.html')

    def test_call_view_loads_create_post(self):
        self.client.login(username='super', password='pass')
        args = {'name': 'name_test', 'start_date': '2018-06-19', 'end_date': '2018-06-27', 'difficulty': 'Easy',
                'category': 'Sport'}
        response = self.client.post('/polls/create/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

#Here onwards, for every view, I'm checking the get and post and the failed posts as well.
class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")

    def test_login_get(self):
        response = self.client.get('/polls/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/login.html')

    def test_login_post_pass(self):
        args = {'username': 'user', 'password': 'pass'}
        response = self.client.post('/polls/login/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_login_post_fail(self):
        args = {'username': 'dfsgsfg', 'password': 'pass'}
        response = self.client.post('/polls/login/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/login.html')

class TestSignUpView(TestCase):
    def test_signup_get(self):
        response = self.client.get('/polls/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/signup.html')

    def test_signup_pass(self):
        args = {'username': 'user', 'password': 'pass'}
        response = self.client.post('/polls/signup/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/login.html')

    def test_signup_fail(self):
        args = {'username': '', 'password': ''}
        response = self.client.post('/polls/signup/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/signup.html')

class TestTournamentView(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name="testTournament", start_date='2018-06-20', end_date='2018-06-27',
                                               difficulty="easy", category="Sports")
        tournament.save()
        questions = ["q1", "q2", "q3"]
        answers = ["a1", "a2", "a3"]
        for q in questions:
            question = Question.objects.create(tournament=tournament, question_text=q,
                                           correct_ans=answers[0])
            answer = Answer.objects.create(question=question, answer_text=answers[0])
            answer.save()
            for a in answers:
                answer = Answer.objects.create(question=question, answer_text=a)
                answer.save()
            question.save()

        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_user(username = "test", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")

    def test_tournament_get(self):
        self.client.login(username='user', password='pass')
        tournament = Tournament.objects.get(name="testTournament")
        response = self.client.get('/polls/tournament/%d' % tournament.id, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/tournament.html')

    def test_tournament_get_completed(self):
        self.client.login(username='user', password='pass')
        tournament = Tournament.objects.get(name="testTournament")
        current_user = Player_Scores.objects.create(username = "user", tournament = tournament.id, current_question = 10, score = 0)
        current_user.save()
        response = self.client.get('/polls/tournament/%d' % tournament.id, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_tournament_post(self):
        self.client.login(username='test', password='pass')
        tournament = Tournament.objects.get(name="testTournament")
        current_user = Player_Scores.objects.create(username = "test", tournament = tournament.id, current_question = 0, score = 0)
        current_user.save()
        response = self.client.post('/polls/tournament/%d' % tournament.id, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/tournament.html')

class TestLogoutView(TestCase):
    def test_signup_get(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/polls/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/login.html')

class TestHighscoreView(TestCase):
    def test_highscores_get(self):
        response = self.client.get('/polls/highscores/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/highscores.html')

class TestViewLoads(TestCase):
    def setUp(self):
        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")

    def test_call_view_loads(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/polls/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_results(self):
        from django.urls import reverse
        response = self.client.get(reverse('polls:login'), format='json')
        self.assertEqual(response.status_code, 200)

class TestResultView(TestCase):
    def setUp(self):
        User.objects.create_user(username = "user", password = "pass")
        User.objects.create_superuser(username="super", email="test@gmail.com", password="pass")

    def test_result_get(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/polls/scores/10', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')