from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class SqlProblem(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    rank = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return f'{self.name} SqlProblem'
        return "Name: " + str(self.name) + " Rank: " + str(self.rank)

# class SqlProblem:
#     def __init__(self,name=None, rank=0):
#         self.name = name
#         self.rank = rank
#
#     def __str__(self):
#         return "Name: " + str(self.name) + " Rank: " + str(self.rank)
