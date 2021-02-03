import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import SqlProblem, UsersProblems, Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
global_logger = logging.getLogger(__name__)


def _reset_sqlproblems_db(user):
    user_problems = UsersProblems.objects.filter(user=user)
    user_problems.delete()


def _init_sqlproblems_db():
    global_logger.error("init_sqlproblems_db called")
    problems = [
        SqlProblem(1, name="Problem1", score=1, type="IN_BAND", difficult='EASY'),
        SqlProblem(2, name="Problem2", score=2, type="IN_BAND", difficult='EASY'),
        SqlProblem(3, name="Problem3", score=3, type="IN_BAND", difficult='EASY'),
        SqlProblem(4, name="Problem4", score=4, type="BLIND", difficult='MEDIUM'),
        SqlProblem(5, name="Problem5", score=5, type="OUT_BAND", difficult='MEDIUM'),
        SqlProblem(6, name="Problem6", score=6, type="BLIND", difficult='HARD'),
        SqlProblem(7, name="Problem7", score=7, type="IN_BAND", difficult='HARD'),
        SqlProblem(8, name="Problem8", score=8, type="IN_BAND", difficult='HARD'),
        SqlProblem(9, name="Problem9", score=9, type="IN_BAND", difficult='HARD'),

    ]
    for problem in problems:
        problem.save()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            _init_sqlproblems_db()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    global_logger.error(" profile view called ")

    if request.method == 'POST':
        print("reset called")
        _reset_sqlproblems_db(request.user.profile)

    user_problems = UsersProblems.objects.filter(user=request.user.profile)
    print(user_problems)
    all_problems = SqlProblem.objects.all()
    print(all_problems)
    rest_of_problems = []
    for problem in all_problems:
        if problem.name not in [user_problem.problem.name for user_problem in user_problems]:
            rest_of_problems.append(problem)
    result = get_profile_progress(request.user.profile)
    all_solved = result[0] + result[1] + result[2]
    context = {
        'user_problems': user_problems,
        'all_problems': all_problems,
        'rest_of_problems': rest_of_problems,
        'easy_solved': result[0],
        'medium_solved': result[1],
        'hard_solved': result[2],
        'score_gained': result[3],
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


def get_profile_progress(user):
    global_logger.error(" get_solved_of_difficult called ")
    user_problems = UsersProblems.objects.filter(user=user)
    hard_solved = 0
    med_solved = 0
    easy_solved = 0
    score = 0
    for problem in user_problems:
        score += problem.problem.score
        if problem.problem.difficult == "Hard":
            hard_solved += 1
        elif problem.problem.difficult == "MEDIUM":
            med_solved += 1
        else:
            easy_solved += 1

    result = [easy_solved, med_solved, hard_solved,score]
    return result


@login_required
def change_password(request,
                    password_change_form=PasswordChangeForm):
    logger = logging.getLogger(__name__)
    logger.error("change_password called :")
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'The password has been changed successfully')
            return redirect('profile')
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
    }
    return render(request, 'users/change_password.html', context)
