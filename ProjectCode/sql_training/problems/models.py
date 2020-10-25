from django.db import models


# Create your models here.
class CheckProblems(models.Model):
    username = models.CharField(max_length=200, null=True)
    problemnumber = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now=True)


class FirstProblem(models.Model):
    input1 = models.CharField(max_length=200, null=True)
    input2 = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'input1: {} input2: {} '.format(self.input1, self.input2)


class SecondProblem(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True, default=0, null=False)
    first_name = models.TextField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.id, self.first_name, self.last_name, self.age}'

    #class Meta:
    #    db_table = 'HR'
