from django.shortcuts import render

# Create your views here.
import logging
from django.shortcuts import render, redirect
from django.db import connections

# Create your views here.
from .models import CheckProblems
from .models import FirstProblem
from collections import namedtuple


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


def first_problem(request):
    context = {
        'problems': []
    }
    # for first time we will do it
    logger = logging.getLogger(__name__)
    logger.error(" problem_login view called ")
    cursor1 = connections['problems_db'].cursor()

    # make data permanent in the database
    # for data in alldata:
    #     data.save(using="problems_db")
    if request.method == 'POST':
        logger.error(" request is Post ")
        input1_request = request.POST.get("input1")
        # input2_request = request.POST.get("input2")
        # logger.error("input1 is: " + input1_request + " input2 is: " + input2_request)
        logger.error("input1 is: " + input1_request)
        # query = """ select input1, input2 from problems_firstproblem where input1 = 'input2_request' input1limit 1 """
        # query = 'select input1, input2 from problems_firstproblem limit 1'
        # query = "select input1, input2 from problems_firstproblem where input1='%s' limit 1"
        # query = 'SELECT * FROM problems_firstproblem WHERE input2 =%s' % input1_request
        # results = FirstProblem.objects.using('problems_db').raw(query)
        # results = FirstProblem.objects.using('problems_db').raw('wwwwwwwwww * FROM problems_firstproblem WHERE input2 = %s',
        #                                                         [input1_request])
        # for result in results:
        #     logger.error(result)

        # result = FirstProblem.objects.raw(using="problems_db"'SELECT * FROM problems_firstproblem')
        with cursor1 as cursor:
            # cursor.execute("select input1, input2 from problems_firstproblem where input1='%s' limit 1" % input1_request)
            # result = cursor.execute("select input1, input2 from problems_firstproblem where input2='%s'" % input1_request)

            # cursor.execute('SELECT * FROM problems_firstproblem WHERE input2=%s' % input1_request)
            # sql = f"SELECT * FROM problems_firstproblem WHERE input2 LIKE '%{input1_request}%';"
            sql = f"SELECT * FROM problems_firstproblem WHERE input2 LIKE '{input1_request}';"

            cursor.execute(sql)

            # cursor.execute('SELECT * FROM problems_firstproblem WHERE input2=?' % input1_request)

            # cursor.execute("select input1, input2 from problems_firstproblem where input2=%s", [input1_request])
            result = cursor.fetchall()
            # result = namedtuplefetchall(cursor)
            logger.error(result)
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


def second_problem(request):
    return render(request, 'problems/2.html')


def third_problem(request):
    return render(request, 'problems/3.html')
