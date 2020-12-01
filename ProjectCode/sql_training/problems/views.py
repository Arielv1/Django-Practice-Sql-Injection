from django.shortcuts import render

# Create your views here.
import logging
import os
import sys
import re
from psycopg2.extensions import quote_ident
import psycopg2

from django.shortcuts import render, redirect
from django.db import connections

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
        Employee(115161598, "Ariel", "Vainshtein", 26),
        Employee(306252136, "Joshua", "Graham", 30),
        Employee(268451234, "Abraham", "Yalkovitch", 28),

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
    item.save()


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


# TODO - implement error checking
'''
    get all information about the table
    remove hint
    answer:
    1 or 1=1
    
    
'''


@login_required
def first_problem(request):
    # fill_employee_database()
    context = {
        'num_items': len(Employee.objects.using('problems_db').all())
    }

    # for first time we will do it
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    cursor1 = connections['problems_db'].cursor()
    if request.method == 'POST':
        # logger.error(" request is Post ")
        input_id_request = request.POST.get("input_id")
        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[1], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[1])

        if input_id_request is not None and input_id_request != "":
            with cursor1 as cursor:
                sql = f"SELECT * FROM db_employees WHERE id = {input_id_request};"
                try:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    context['result'] = result
                    context['num_resulted_items'] = len(result)
                    logger.error(result)
                    cursor.close()
                except:
                    pass

    return render(request, 'problems/1.html', context)


'''
    result 
    First Name: %
    Last Name:: %
'''


def escaping(a_string):
    escaped = a_string.translate(str.maketrans({"=": r"\=",
                                                "]": r"\]",
                                                "\\": r"\\",
                                                "^": r"\^",
                                                ";": r"\;",
                                                "*": r"\*",
                                                ".": r"\."}))
    return escaped


@login_required
def second_problem(request):
    fill_employee_database()

    cursor1 = connections['problems_db'].cursor()
    context = {'num_items': len(Employee.objects.using('problems_db').all())}

    if request.method == 'POST':
        first_name_request = request.POST.get("first_name")
        last_name_request = request.POST.get("last_name")
        first_name_request = escaping(first_name_request)
        last_name_request = escaping(last_name_request)

        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[2], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[2])
        with cursor1 as cursor:
            sql = f"SELECT id, first_name, last_name FROM db_employees WHERE first_name LIKE '{first_name_request}' and last_name LIKE '{last_name_request}'"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                context['result'] = result
                context['num_resulted_items'] = len(result)
            except:
                pass

    return render(request, 'problems/2.html', context)


'''
    Step #1:
    1 UNION SELECT 1,table_schema,table_name,2
    FROM information_schema.tables
    WHERE table_schema LIKE 'public'
    
    Step #2:
    1; select * from db_clothing_shop
'''


@login_required
def third_problem(request):
    fill_clothing_store_db()
    key_words = ['or', 'and', ';', 'inner join', '=']
    context = {
        'num_items': len(ClothingStore.objects.using('problems_db').all()),
    }
    logger = logging.getLogger(__name__)
    cursor1 = connections['problems_db'].cursor()

    # add columns to database
    # fill_clothing_store_db()
    # ClothingStore.objects.all().delete()
    if request.method == 'POST':
        with cursor1 as cursor:
            item_name_request = request.POST.get("item_name")
            print(item_name_request)
            for kw in key_words:
                if kw in item_name_request:
                    logger.error("changing item_name_request")
                    item_name_request = "1"
                    break
            sql = f"SELECT * FROM db_clothing_store WHERE barcode = '{item_name_request}'"
            err = Exception
            try:
                cursor.execute(sql)
            except Exception as e:
                sql = f"SELECT * FROM db_clothing_store WHERE item_name LIKE 'a'"
                cursor.execute(sql)
                err = e
            result = cursor.fetchall()
            print(result)
            cursor.close()
            context['result'] = result
            context['num_resulted_items'] = len(result)
            context['error'] = err

    return render(request, 'problems/3.html', context)


'''
    objective: get the name of the table
'''


@login_required
def forth_problem(request):
    global_logger.error(" forth_problem view called ")
    context = {'message': "Out of stock"}
    # fill_vehicle_db()

    cursor2 = connections['problems_db'].cursor()
    if request.method == 'POST':
        manufacturer_request = request.POST.get("input_manufacturer")
        user_answer = request.POST.get("problem_answer")
        is_answer = check_answer_input(answers[4], str(user_answer))
        if is_answer:
            update_answer_for_user(request.user, problem_name=problems_names[4])
        with cursor2 as cursor:
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
    logger = logging.getLogger(__name__)
    cursor = connections['problems_db'].cursor()

    context = {
        'items': ClothingItem.get_values(),
        'num_items': len(ClothingStore.objects.using('problems_db').all()),
    }
    # add rows to the database

    if request.method == 'POST':
        item_name_request = request.POST.get("item_select")
        logger.error(item_name_request)
        sql = f"SELECT * FROM db_clothing_store WHERE item_name LIKE '{item_name_request}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        context['result'] = result
        context['num_items'] = len(result)

    return render(request, 'problems/5.html', context)


@login_required
def sixth_problem(request):
    init_secret_db()

    context = {
        'secret_value': BlindSecret.objects.filter(id=1)[0].secret
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
    # print(request.method)
    # print(request.headers)
    # print(request.headers["User-Agent"])
    context = {}
    # input_first_name = request.POST.get("input_first_name")
    cursor2 = connections['problems_db'].cursor()
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")
    cursor2 = connection.cursor()
    if request.method == 'POST':
        input_first_name = request.POST.get("input_first_name")
        with cursor2 as cursor:
            print("Before input: {} ".format(input_first_name))
            # input_first_name = quote_ident(input_first_name, connection)
            # input_first_name = re.escape(input_first_name)
            # print("After input: {} ".format(input_first_name))
            sql = f"SELECT * FROM db_employees WHERE first_name LIKE '{input_first_name}';"
            print(sql)
            cursor.execute(sql)
            # cursor.execute(f"select * FROM db_employees WHERE \"last_name\" LIKE %s;" % quote_ident(input_first_name, connection))
            result = cursor.fetchall()
            context['result'] = result
            if result is not None and len(result) != 0:
                context['message'] = "There's Employee With This Name"
            else:
                context['message'] = "Not Good User-Agent"
            cursor.close()
    return render(request, 'problems/7.html', context)


@login_required
def eighth_problem(request):
    fill_employee_database()

    context = {
        'items': ClothingItem.get_values(),
        'num_items': len(Employee.objects.using('problems_db').all())
    }
    print(context['items'][0])
    if request.method == 'POST':
        pass

    return render(request, 'problems/8.html', context)


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
