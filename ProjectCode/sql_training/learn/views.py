from django.shortcuts import render

# Create your views here.


def learn(request):
    return render(request, 'learn/learn.html')


def inband(request):
    return render(request, 'learn/inband.html')


def blind(request):
    return render(request, 'learn/blind.html')


def outband(request):
    return render(request, 'learn/outband.html')