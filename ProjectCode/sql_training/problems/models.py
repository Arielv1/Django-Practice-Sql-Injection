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
    name = models.TextField(max_length=200, primary_key=True, unique=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'input1: {} input2: {} '.format(self.name, self.description)
