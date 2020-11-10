from django.urls import path
from . import views


urlpatterns = [
    path('login_problem', views.problem_login, name='login_problem'),
    path('1', views.first_problem, name='first'),
    path('2', views.second_problem, name='second'),
    path('3', views.third_problem, name='third'),
    path('4', views.forth_problem, name='forth'),
    path('5', views.fifth_problem, name='fifth'),
]
