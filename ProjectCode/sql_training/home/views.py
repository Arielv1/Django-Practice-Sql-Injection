import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ProblemReference, Difficulty, InjectionTypes, ProblemData
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError


def home(request):
    logger = logging.getLogger(__name__)
    logger.error(" home view called ")

    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


# todo Setup AWS Email when we can. and add support email.
def contact_us(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('from_email', '')
        support_email = ""
        name = request.POST.get('name', '')

        from_email = request.POST.get('from_email', '')
        # if subject and message and from_email:
        #     if name:
        #         subject = "{} - {}".format(name, subject)
        #     try:
        #         send_mail(subject, message, from_email, [support_email])
        #     except BadHeaderError:
        #         return HttpResponse('Invalid header found.')
        #     messages.success(request, f'Thanks for the Email')
        #     return redirect('home')
        # else:
        #     messages.error(request, f'Please fill Subject and message')
        #     return redirect('contact_us')
    return render(request, 'home/contact_us.html')


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
