import django_filters
from .models import SqlProblem
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class SqlProblemFilter(django_filters.FilterSet):
    # filterset_class = SqlProblem
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = SqlProblem
        fields = '__all__'
        exclude = 'user'


# class SqlProblemFilter(SingleTableMixin, FilterView):
#     table_class = SqlProblemTable
#     model = SqlProblem
#     template_name = "users/profile.html"
#     filterset_class = SqlProblem
#     class Meta:
#         model = SqlProblem
#         fields = ["name", "rank"]
