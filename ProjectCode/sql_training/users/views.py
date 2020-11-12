import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import SqlProblem, UsersProblems, Profile, Hotel

'''
def display_hotel_images(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        Hotels = Hotel.objects.filter(name__startswith="a")
        return render(request, 'users/display.html', {'hotel_images' : Hotels})
        '''

#     # Create your views here.
# def hotel_image_view(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             current_user = request.user
#             logger = logging.getLogger(__name__)
#             Profiles = Profile.objects.get(user=current_user.id)
#             logger.error(Profiles)
#             form.save(commit=False)
#             return redirect('success')
#     else:
#         form = ImageForm()
#     return render(request, 'users/index.html', {'form': form})


def success(request):
    logger = logging.getLogger(__name__)

    return HttpResponse('successfully uploaded')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def create_problems():
    logger = logging.getLogger(__name__)
    logger.error(" create_problems called ")
    SqlProblem(name="problem1").save()
    SqlProblem(name="problem2").save()
    SqlProblem(name="problem3").save()
    SqlProblem(name="problem4").save()
    SqlProblem(name="problem5").save()
    SqlProblem(name="problem6").save()


@login_required
def profile(request):
    if request.method == 'POST':
        # instance=request.user fill the fields with the user data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been been updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    user_problems = UsersProblems.objects.filter(user=request.user.profile)
    context = {
            'user_problems': user_problems,
            'user_form': user_form,
            'profile_form': profile_form
        }
    return render(request, 'users/profile.html', context)
