import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Difficulty, InjectionTypes, ProblemsContentTable
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
import  datetime


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def contact_us(request):
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


def _fill_problem_references():
    items = [
        ProblemsContentTable(1, Difficulty.EASY.value, 'problems/1', 'InBand - Introduction', 'InBand'),
        ProblemsContentTable(2, Difficulty.EASY.value, 'problems/2', 'InBand - Partial Escaping', 'InBand'),
        ProblemsContentTable(3, Difficulty.MEDIUM.value, 'problems/3', 'InBand - Complete Problem', 'InBand'),
        ProblemsContentTable(4, Difficulty.MEDIUM.value, 'problems/4', 'Blind Injection', 'Blind'),
        ProblemsContentTable(5, Difficulty.MEDIUM.value, 'problems/5', 'OutBand Injection', 'OutBand'),
        ProblemsContentTable(6, Difficulty.HARD.value, 'problems/6', 'Blind - Crack The Safe', 'Blind'),
        ProblemsContentTable(7, Difficulty.HARD.value, 'problems/7', 'Blind - User Agents', 'Blind'),
        ProblemsContentTable(8, Difficulty.HARD.value, 'problems/8', 'InBand - Privilege Bypass', 'InBand'),
        ProblemsContentTable(9, Difficulty.HARD.value, 'problems/9', 'Combined - Cookies', 'OutBand + InBand'),
    ]
    for data in items:
        data.save()
    return items


@login_required
def problems_list(request):
    context = {'problem_list': _fill_problem_references()}
    request.session['loginForm'] = False
    request.session['adminLogged'] = False
    response = render(request, "home/problems.html", context)

    response.set_cookie('connection_time', datetime.datetime.now())
    response.set_cookie('cookie_ready_time', datetime.datetime.now() + datetime.timedelta(hours=1))
    response.set_cookie('show_login', False)

    return response
