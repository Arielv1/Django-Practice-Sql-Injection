from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    sqlproblems = models.ManyToManyField('SqlProblem', through='UsersProblems')


class SqlProblem(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    users = models.ManyToManyField('Profile', through='UsersProblems')


class UsersProblems(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(SqlProblem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'problem']
