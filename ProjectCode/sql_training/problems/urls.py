from django.urls import path
from . import views


urlpatterns = [
    path('login_problem', views.problem_login, name='login_problem'),

]