from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='profile_pics/delete_this/')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    sqlproblems = models.ManyToManyField('SqlProblem', through='UsersProblems')


    def __str__(self):
        return f"{self.user, self.image_name, self.image, self.sqlproblems}"

    def save(self, *args, **kwargs):
        # run the save of the default function of save
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class SqlProblem(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    users = models.ManyToManyField('Profile', through='UsersProblems')


class UsersProblems(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(SqlProblem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'problem']
