import django_tables2 as tables
from .models import SqlProblem


class SqlProblemTable(tables.Table):
    class Meta:
        model = SqlProblem
        template_name = "django_tables2/bootstrap.html"




