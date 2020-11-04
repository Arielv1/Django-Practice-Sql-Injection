import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import SqlProblem, UsersProblems, Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def create_problems():
    logger = logging.getLogger(__name__)
    logger.error(" create_problems called ")
    SqlProblem(name="problem1").save()
    SqlProblem(name="problem2").save()
    SqlProblem(name="problem3").save()
    SqlProblem(name="problem4").save()
    SqlProblem(name="problem5").save()
    SqlProblem(name="problem6").save()


@login_required
def profile(request):
    logger = logging.getLogger(__name__)
    logger.error(" profile view called ")
    # create_problems()
    user = request.user
    print(user)
    # p1 = SqlProblem.objects.get(name="problem1")
    # UsersProblems(user=user.profile, problem=p1).save()
    # all = UsersProblems.objects.all()
    # all.delete()
    user_problems = UsersProblems.objects.filter(user=user.profile)
    print(user_problems)
    # sqlproblems = SqlProblem.objects.all()
    # sqlproblems = SqlProblem.objects.filter(user=user)
    # logger.error(" User is: " + str(user.username) + "sqlproblems: " + str(sqlproblems))

    # table = SqlProblemTable(sqlproblems)
    #
    # filter = SqlProblemFilter(request.GET, queryset=sqlproblems)
    # sqlproblems = filter.qs
    # # sorted = request.query_params.get('sort', '')
    # sorted = request.GET.get('sort', '')
    # # print("sorted is : " + str(sorted))
    # if sorted:
    #     # print(" we want to sort lets check it")
    #     if sorted == 'name':
    #         # print(" we want to sort of name")
    #         sqlproblems = sqlproblems.order_by('name')
    #     # elif sorted == 'rank':
    #     #     # print(" we want to sort of rank")
    #     #     sqlproblems = sqlproblems.order_by('rank')
    #
    # table = SqlProblemTable(sqlproblems)
    context = {'user_problems': user_problems}
    # context = {"table": table, "filter": filter, 'sqlproblems': sqlproblems}
    # return render(request, 'users/profile.html', {"filter": filter})
    return render(request, 'users/profile.html', context)
    # return render(request, 'users/profile.html', {"table": table})

# class FilteredSqlProblemListView(LoginRequiredMixin, tables.SingleTableView):
# class FilteredSqlProblemListView(LoginRequiredMixin, tables.SingleTableView, FilterView, ListView):
#     table_class = SqlProblemTable
#     queryset = SqlProblem.objects.all()
#     template_name = "users/profile.html"
#     filterset_class = SqlProblemFilter
#
#     def get_context_data(self, **kwargs):
#         filter = SqlProblemFilter(self.request.GET, queryset=SqlProblem.objects.all())
#         context = super(FilteredSqlProblemListView, self).get_context_data()
#         filter = filter.qs
#         context['filter'] = filter
#         return context
