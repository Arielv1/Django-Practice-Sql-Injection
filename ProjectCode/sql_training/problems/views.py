from django.shortcuts import render

# Create your views here.
import logging
import os
import sys

print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25} | __directory__={3:<25}'.format(__file__, __name__,
                                                                                                 str(__package__),
                                                                                                 str(os.getcwd())))
from django.shortcuts import render, redirect
from django.db import connections

# Create your views here.
from .models import CheckProblems
from .models import *
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from users.models import UsersProblems, SqlProblem

# TODO put each problem his answer here

answers = ["something", "this is_the_answer", "second answer"]
problems_names = ["no problem", "problem1", "problem2", "problem3", "problem4"]
global_logger = logging.getLogger(__name__)
alldata = [
    FirstProblem(input1="1", input2="2"),
    FirstProblem(input1="else", input2="2"),
    FirstProblem(input1="something", input2="something2"),
    FirstProblem(input1="elasdasdse", input2="something3"),
    FirstProblem(input1="asdas", input2="someasdsathing4"),
    FirstProblem(input1="sad", input2="something5"),
    FirstProblem(input1="scxzc", input2="something6"),
    FirstProblem(input1="somzxczxcething", input2="something8"),
    FirstProblem(input1="this is_the_answer", input2="answer"),
]


def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def check_answer_input(real_answer, user_answer):
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    if real_answer == user_answer:
        logger.error(" Good job the answer is good ")
        return True
    else:
        return False


def update_answer_for_user(user, problem_name):
    global_logger.error("update_answer_for_user called")
    print(user)
    print(problem_name)
    problem = SqlProblem.objects.get(name=problem_name)
    UsersProblems(user=user.profile, problem=problem).save()


@login_required
def first_problem(request):
    context = {
        'problems': []
    }
    # for first time we will do it
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    cursor1 = connections['problems_db'].cursor()

    # alldata_first_problem = FirstProblem.objects.using('problems_db').all()
    # print(alldata_first_problem)
    # alldata_first_problem.delete()
    # # make data permanent in the database
    # for data in alldata:
    #     data.save(using="problems_db")
    if request.method == 'POST':
        # logger.error(" request is Post ")
        input1_request = request.POST.get("input1")
        user_answer = request.POST.get("problem_answer")
        logger.error("problem_answer is: " + str(user_answer))
        logger.error("input1 is: " + str(input1_request))
        is_answer = check_answer_input(answers[1], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[1])

        if input1_request is not None and input1_request != "":
            logger.error("user entered input 1")
            with cursor1 as cursor:
                sql = f"SELECT * FROM problems_firstproblem WHERE input2 LIKE '{input1_request}';"
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.error(result)
                # logger.error("result of sql querry: " + result.__str__())
                cursor.close()
                # allProblems = []
                # for data in result:
                #     allProblems.append(FirstProblem(input1=data.input1,input2=data.input2))
                # context = {
                #     'problems': allProblems
                # }
                # if result is not None and len(result) != 0:
                #     if result[0].input1 == "this is_the_answer" and result[0].input2 == "answer":
                #         logger.error("GOOOOOOOOOD JOBBBBBBBB")
                #     else:
                #         logger.error("memememememememememememe WRONGGGGGGGGGGGGGG")
                # else:
                #     logger.error("result is None Probably Or Size = 0")

    return render(request, 'problems/1.html', context)


def second_problem_database():
    employees = [
        SecondProblem(205476765, "Ariel", "Vainshtein", 25),
        SecondProblem(306252136, "Abe", "Kelson", 22),
        SecondProblem(268451234, "Abraham", "Yalkovitch", 28),
    ]
    for data in employees:
        data.save(using="problems_db")


'''
    Input fields: first_name & last_name
    To perform injection: place wildcards in both fields to get all users:
    First Name: %
    Last Name: %
'''


@login_required
def second_problem(request):
    context = dict()
    logger = logging.getLogger(__name__)
    cursor1 = connections['problems_db'].cursor()

    # add columns to database
    # second_problem_database()

    if request.method == 'POST':
        first_name_request = request.POST.get("first_name")
        last_name_request = request.POST.get("last_name")
        user_answer = request.POST.get("problem_answer")
        logger.error("problem_answer is: " + str(user_answer))
        logger.error("first_name input is: " + str(first_name_request))
        is_answer = check_answer_input(answers[2], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[2])
        if first_name_request is not None and first_name_request != "":
            logger.error("user entered first name")
            with cursor1 as cursor:

                # id_request = request.POST.get("id_request")
                # sql = f"SELECT '{input_request}' FROM problems_secondproblem WHERE first_name LIKE 'Ariel'"
                sql = f"SELECT id, first_name, last_name FROM problems_secondproblem WHERE first_name LIKE '{first_name_request}' and last_name LIKE '{last_name_request}'"
                # sql = f"SELECT * FROM problems_secondproblem WHERE id={id_request}"
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.error("result of sql query " + result.__str__())
                cursor.close()
                context = {'raw_sql': sql,
                           'result': result,
                           'input_request': first_name_request}
    return render(request, 'problems/2.html', context)


@login_required
def third_problem_database():
    employees = [
        ThirdProblem(803654786, "T-Shirt", "Nike", 25.23),
        ThirdProblem(987124123, "Jeans", "H&o", 22.10),
        ThirdProblem(300125487, "Sweat Pants", "Diadora", 28.99),
    ]
    for data in employees:
        data.save(using="problems_db")


'''
    Input: bigint barcode field
    Output: Item properties
    
'''


@login_required
def third_problem(request):
    key_words = ['or', 'and', 'union', 'inner join']
    context = dict()
    logger = logging.getLogger(__name__)
    cursor1 = connections['problems_db'].cursor()

    # add columns to database
    # third_problem_database()

    if request.method == 'POST':
        with cursor1 as cursor:
            item_name_request = request.POST.get("item_name").lower()
            logger.error("after lower")
            logger.error(item_name_request)

            for kw in item_name_request:
                # logger.error(kw)
                if kw in key_words:
                    logger.error("changing item_name_request")
                    item_name_request = "1"
                    break
            logger.error("before running sql query")
            logger.error(item_name_request)
            sql = f"SELECT * FROM db_items WHERE barcode = {item_name_request}"

            err = Exception
            try:
                cursor.execute(sql)
            except Exception as e:
                sql = f"SELECT * FROM db_items WHERE item_name LIKE 'a'"
                cursor.execute(sql)
                err = e
                logger.error("we got error")
                print(err)
            result = cursor.fetchall()
            logger.error("result of sql query " + result.__str__())
            logger.error(result)
            cursor.close()
            context = {'raw_sql': sql,
                       'result': result,
                       'item_name_request': item_name_request,
                       'error': err}
    return render(request, 'problems/3.html', context)


@login_required
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
