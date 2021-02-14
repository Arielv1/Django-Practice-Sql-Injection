from django.db import connections
from django.shortcuts import render
from .models import DummyUser


def _init_dummy_db():
    items = [
        DummyUser('user1', 'password1'),
        DummyUser('user2', 'password2')
    ]

    for item in items:
        item.save(using='problems_db')


def learn(request):
    _init_dummy_db()
    return render(request, 'learn/learn.html')


def inband(request):
    context = {'num_items': len(DummyUser.objects.using('problems_db').all())}
    cursor = connections['problems_db_read_user'].cursor()
    if request.method == 'POST' and 'btnForm1' in request.POST:
        input1_request = request.POST.get("input1")
        input2_request = request.POST.get("input2")
        sql = f"SELECT * FROM db_dummy_users WHERE username LIKE '{input1_request}' AND password LIKE '{input2_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result1'] = result
            context['num_resulted_items'] = len(result)
        except Exception as e:
            context['error1'] = e
    elif request.method == 'POST' and 'btnForm2' in request.POST:
        input3_request = request.POST.get("input3")
        sql = f"{input3_request}"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result2'] = result
        except Exception as e:
            context['error2'] = e
    cursor.close()
    return render(request, 'learn/inband.html', context)


def blind(request):
    return render(request, 'learn/blind.html')


def outband(request):
    return render(request, 'learn/outband.html')


def tools(request):
    return render(request, 'learn/tools.html')


def prevent_sqli(request):
    return render(request, 'learn/prevent_sqli.html')