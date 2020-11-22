import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import SqlProblem, UsersProblems, Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    user_problems = UsersProblems.objects.filter(user=request.user.profile)
    all_problems = SqlProblem.objects.filter()
    rest_of_problems = []
    for problem in all_problems:
        if problem.name not in [user_problem.problem.name for user_problem in user_problems]:
            rest_of_problems.append(problem)
    result = get_solved_of_difficult(request.user.profile)
    all_solved = result[0] + result[1] + result[2]
    context = {
        'user_problems': user_problems,
        'all_problems': all_problems,
        'rest_of_problems': rest_of_problems,
        'easy_solved': result[0],
        'medium_solved': result[1],
        'hard_solved': result[2],
        'all_solved': all_solved,

    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
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

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/edit_profile.html', context)


def get_solved_of_difficult(user):
    user_problems = UsersProblems.objects.filter(user=user)
    hard_solved = 0
    med_solved = 0
    easy_solved = 0
    for problem in user_problems:
        if problem.problem.difficult == "Hard":
            hard_solved += 1
        elif problem.problem.difficult == "MEDIUM":
            med_solved += 1
        else:
            easy_solved += 1

    result = [easy_solved, med_solved, hard_solved]
    return result
