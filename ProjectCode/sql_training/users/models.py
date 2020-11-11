from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='profile_pics/delete_this/')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50, default='default')
    image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')
    sqlproblems = models.ManyToManyField('SqlProblem', through='UsersProblems')

    def __str__(self):
        return f"{self.user, self.image_name, self.image, self.sqlproblems}"

class SqlProblem(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    users = models.ManyToManyField('Profile', through='UsersProblems')


class UsersProblems(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(SqlProblem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'problem']
