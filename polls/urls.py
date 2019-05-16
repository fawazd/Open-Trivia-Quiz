from django.urls import path
from django.conf.urls import url

from . import views
from polls.views import HomeView, CreateTournamentView, LoginView, SignUpView, TournamentView, LogoutView, HighscoresView, ResultsView

app_name = 'polls'
urlpatterns = [
    path('tournament/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('feedback/', TournamentView.as_view(), name='feedback'),
    path('', TournamentView.as_view(), name='check_answer'),
    path('create/', CreateTournamentView.as_view(), name='create'),
    path('create_tourny/', CreateTournamentView.as_view(), name='create_tourny'),
    path('index/', HomeView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('highscores/', HighscoresView.as_view(), name='highscores'),
    path('', SignUpView.as_view(), name='create_user'),
    path('scores/<int:score>', ResultsView.as_view(), name='results'),
]
