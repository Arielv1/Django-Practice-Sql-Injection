import logging
from django.shortcuts import render, redirect
from home.models import ProblemReference, Difficulty, InjectionTypes, ProblemData
from django.contrib.auth.decorators import login_required


def home(request):
    logger = logging.getLogger(__name__)
    logger.error(" home view called ")

    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')






def fill_references():
    items = [
        ProblemData(1, Difficulty.EASY.value, 'problems/1', 'First Problem', 'Classic'),
        ProblemData(2, Difficulty.MEDIUM.value, 'problems/2', 'Second Problem', 'Classic'),
        ProblemData(3, Difficulty.MEDIUM.value, 'problems/3', 'Third Problem', 'Classic'),
        ProblemData(4, Difficulty.HARD.value, 'problems/4', 'Forth Problem', 'Classic'),
        ProblemData(5, Difficulty.HARD.value, 'problems/5', 'Fifth Problem', 'Classic'),
        ProblemData(6, Difficulty.HARD.value, 'problems/6', 'Sixth Problem', 'Classic'),
        ProblemData(7, Difficulty.HARD.value, 'problems/7', 'Seventh Problem', 'Classic'),

    ]
    for data in items:
        data.save()

    return items

@login_required
def problems_list(request):
    context = {'problem_list': fill_references()}

    return render(request, "home/problems.html", context)