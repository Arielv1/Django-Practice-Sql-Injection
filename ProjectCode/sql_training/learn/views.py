from django.db import connections
from django.shortcuts import render
from .models import DummyUser


# Create your views here.
def init_dummy_db():
    items = [
        DummyUser(username='user1', password='password1'),
        DummyUser(username='user2', password='password2')
    ]
    for item in items:
        item.save(using='learning_db')


def learn(request):
    # DummyUser.objects.all().delete()
    # init_dummy_db()
    # print(DummyUser.objects.all())
    return render(request, 'learn/learn.html')


def inband(request):
    # print(DummyUser.objects.using('learning_db').all())
    context = {'num_items': len(DummyUser.objects.using('learning_db').all())}
    if request.method == 'POST':
        input1_request = request.POST.get("input1")
        input2_request = request.POST.get("input2")
        cursor = connections['learning_db'].cursor()
        sql = f"SELECT * FROM db_dummy_users WHERE username LIKE '{input1_request}' AND password LIKE '{input2_request}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            context['result'] = result
            context['num_resulted_items'] = len(result)
            cursor.close()
        except:
            pass

    return render(request, 'learn/inband.html', context)


def blind(request):
    return render(request, 'learn/blind.html')


def outband(request):
    return render(request, 'learn/outband.html')


def tools(request):
    return render(request, 'learn/tools.html')


def protection(request):
    return render(request, 'learn/protection.html')


def check(request):
    return render(request, 'learn/check.html')
