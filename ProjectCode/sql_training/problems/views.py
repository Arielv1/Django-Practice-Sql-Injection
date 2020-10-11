from django.shortcuts import render

# Create your views here.
import logging
from django.shortcuts import render, redirect


# Create your views here.


def problem_login(request):
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    if request.method == 'POST':
        logger.error(" request is Post ")
        # first_name = request['username'].value()
        logger.error(request)
        logger.error(request.body)
        logger.error(request.content_params)
        # logger.error(dir(request))
        # logger.error(dir(request.body))
        # logger.error(request.body.__getitem__())
        logger.error(request.POST.get("username"))

    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         messages.success(request, f'Your account has been created! You are now able to log in')
    #         return redirect('login')
    # else:
    #     form = UserRegisterForm()
    return render(request, 'problems/login.html')


def first_problem(request):
    return render(request, 'problems/1.html')


def second_problem(request):
    return render(request, 'problems/2.html')


def third_problem(request):
    return render(request, 'problems/3.html')