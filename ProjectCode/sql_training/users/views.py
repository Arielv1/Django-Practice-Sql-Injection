from django.shortcuts import render
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import render
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView
from django.views.generic import ListView
from django.contrib.auth.models import User

from .forms import UserRegisterForm
from .models import SqlProblem

# Create your views here.
from .tables import SqlProblemTable
from .filters import SqlProblemFilter


p1 = SqlProblem(name="First problem", rank=1)
p2 = SqlProblem(name="Second problem", rank=2)
p3 = SqlProblem(name="Third problem", rank=3)
p4 = SqlProblem(name="Fourth problem", rank=4)

problems = [p1, p3, p4, p2]


# class PersonListView(SingleTableView):
#     model = SqlProblem
#     table_class = SqlProblemTable(problems)
#     template_name = "users/profile.html"


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


@login_required
def profile(request):
    logger = logging.getLogger(__name__)
    logger.error(" profile view called ")
    user = request.user
    sqlproblems = SqlProblem.objects.all()
    # sqlproblems = SqlProblem.objects.filter(user=user)
    # logger.error(" User is: " + str(user.username) + "sqlproblems: " + str(sqlproblems))

    table = SqlProblemTable(sqlproblems)

    filter = SqlProblemFilter(request.GET, queryset=sqlproblems)
    sqlproblems = filter.qs
    # sorted = request.query_params.get('sort', '')
    sorted = request.GET.get('sort', '')
    # print("sorted is : " + str(sorted))
    if sorted:
        # print(" we want to sort lets check it")
        if sorted == 'name':
            # print(" we want to sort of name")
            sqlproblems = sqlproblems.order_by('name')
        elif sorted == 'rank':
            # print(" we want to sort of rank")
            sqlproblems = sqlproblems.order_by('rank')

    table = SqlProblemTable(sqlproblems)

    context = {"table": table, "filter": filter, 'sqlproblems': sqlproblems}
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