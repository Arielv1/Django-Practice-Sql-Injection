import logging
from django.shortcuts import render, redirect

# Create your views here.
from home.models import ProblemReference, Difficulty, InjectionTypes
from django.contrib.auth.decorators import login_required


def home(request):
    logger = logging.getLogger(__name__)
    logger.error(" home view called ")

    # context = {
    #      'customers': Customer.objects.all()
    # }
    #  logger.error(" first Customer :" + Customer.objects.first().first_name)

    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def learn(request):
    return render(request, 'home/learn.html')

@login_required
def problems_list(request):
    context = {'problem_list':
                   [ProblemReference(Difficulty.EASY, "First Problem", InjectionTypes.IN_BAND.value, "problems/1"),
                    ProblemReference(Difficulty.MEDIUM, "Second Problem", InjectionTypes.IN_BAND.value, "problems/2"),
                    ProblemReference(Difficulty.HARD, "Third Problem", InjectionTypes.UNION.value, "problems/3"),
                    ProblemReference(Difficulty.EASY, "Forth Problem", InjectionTypes.BLIND.value, "problems/4"),
                    ProblemReference(Difficulty.MEDIUM, "Fifth Problem", InjectionTypes.IN_BAND.value, "problems/5"),
                    ProblemReference(Difficulty.EASY, "Login Problem", InjectionTypes.IN_BAND.value, "problems"
                                                                                                     "/login_problem")],
               'EASY': Difficulty.EASY,
               'MEDIUM': Difficulty.MEDIUM,
               'HARD': Difficulty.HARD,
               }
    return render(request, 'home/problems.html', context)
