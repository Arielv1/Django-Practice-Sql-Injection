import logging
from django.shortcuts import render, redirect


# Create your views here.


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