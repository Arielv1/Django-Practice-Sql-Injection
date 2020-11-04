import django_tables2 as tables
import django_filters
from .models import SqlProblem
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


# class SqlProblemTable(tables.Table):
#     name = tables.Column()
#     rank = tables.Column()

class SqlProblemTable(tables.Table):
    class Meta:
        model = SqlProblem
        template_name = "django_tables2/bootstrap.html"
        # fields = ("name", "rank",)




