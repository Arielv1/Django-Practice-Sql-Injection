import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Difficulty, InjectionTypes, ProblemsContentTable
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
import logging, datetime

global_logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def contact_us(request):
    global_logger.error(" contact_us view called ")
    if request.method == 'POST':
        name = request.POST.get('name', '')
        user_email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        support_email = ['hamami2010@gmail.com']
        if subject and message:
            if name:
                subject = "{} - {}".format(name, user_email)
            try:
                if user_email:
                    message = "Sent from : {} \n {}".format(user_email, message)
                send_mail(subject=subject, message=message, recipient_list=support_email, from_email=None)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, f'Thanks for the Email')
            return redirect('home')
        else:
            messages.error(request, f'Please fill Subject and message')
            return redirect('contact_us')
    return render(request, 'home/contact_us.html')


def fill_references():
    items = [
        ProblemsContentTable(1, Difficulty.EASY.value, 'problems/1', 'First Problem', 'In Band - Introduction'),
        ProblemsContentTable(2, Difficulty.EASY.value, 'problems/2', 'Second Problem', 'In Band - Escaping'),
        ProblemsContentTable(3, Difficulty.MEDIUM.value, 'problems/3', 'Third Problem', 'In Band'),
        ProblemsContentTable(4, Difficulty.MEDIUM.value, 'problems/4', 'Fourth Problem', 'Blind'),
        ProblemsContentTable(5, Difficulty.MEDIUM.value, 'problems/5', 'Fifth Problem', 'Out Band'),
        ProblemsContentTable(6, Difficulty.HARD.value, 'problems/6', 'Sixth Problem', 'Blind'),
        ProblemsContentTable(7, Difficulty.HARD.value, 'problems/7', 'Seventh Problem', 'Classic'),
        ProblemsContentTable(8, Difficulty.HARD.value, 'problems/8', 'Eighth Problem', 'In Band'),
        ProblemsContentTable(9, Difficulty.HARD.value, 'problems/9', 'Ninth Problem', 'TBD'),
    ]
    for data in items:
        data.save()
    return items


@login_required
def problems_list(request):
    context = {'problem_list': fill_references()}
    response = render(request, "home/problems.html", context)

    response.set_cookie('connection_time', datetime.datetime.now())
    response.set_cookie('cookie_ready_time', datetime.datetime.now() + datetime.timedelta(hours=1))
    response.set_cookie('autherized', False)
    response.set_cookie('show_login', 0==1)
    return response
