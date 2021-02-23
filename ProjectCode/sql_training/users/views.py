from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from pylint.checkers.typecheck import _

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import SqlProblem, UsersProblems, Profile
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.utils import timezone


def _reset_sqlproblems_db(user):
    user_problems = UsersProblems.objects.filter(user=user)
    user_problems.delete()


def _init_sqlproblems_db():
    problems = [
        SqlProblem(1, name="1. InBand - Introduction", score=1, type="InBand", difficult='EASY'),
        SqlProblem(2, name="2. InBand - Partial Escaping", score=2, type="InBand", difficult='EASY'),
        SqlProblem(3, name="3. InBand - Complete Problem", score=3, type="InBand", difficult='EASY'),
        SqlProblem(4, name="4. Blind Injection", score=4, type="Blind", difficult='MEDIUM'),
        SqlProblem(5, name="5. OutBand Injection", score=5, type="OutBand", difficult='MEDIUM'),
        SqlProblem(6, name="6. Blind - Crack The Safe", score=6, type="Blind", difficult='HARD'),
        SqlProblem(7, name="7. Blind - User Agents", score=7, type="Blind", difficult='HARD'),
        SqlProblem(8, name="8. InBand - Privilege Bypass", score=8, type="InBand", difficult='HARD'),
        SqlProblem(9, name="9. Combined - Cookies", score=9, type="	OutBand + InBand", difficult='HARD'),

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
    if request.method == 'POST':
        _reset_sqlproblems_db(request.user.profile)

    user_problems = UsersProblems.objects.filter(user=request.user.profile)
    all_problems = SqlProblem.objects.all()
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
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account details have been updated')
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
def change_password(request, password_change_form=PasswordChangeForm):
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.password_changed = timezone.now()
            profile.save()
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

@csrf_protect
def reset_password(request, is_admin_site=False,
                   template_name='users/password_reset_form.html',
                   email_template_name='users/password_reset_email_to_user.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   success_url=reverse_lazy('password_reset_done'),
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'domain_override': '127.0.0.1:8000',
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override='127.0.0.1:8000')
            form.save(**opts)
            return redirect('password_reset_done')
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)