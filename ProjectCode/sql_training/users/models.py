from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')
    sqlproblems = models.ManyToManyField('SqlProblem', through='UsersProblems')

    def __str__(self):
        return f"{self.user, self.image, self.sqlproblems}"

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
    score = models.IntegerField(default=1)
    TYPE_CHOICES = (
        ("BLIND", "Blind"),
        ("IN_BAND", "In_Band"),
        ("OUT_BAND", "Out_Band")
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='BLIND')
    Difficult_CHOICES = (
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard")
    )

    difficult = models.CharField(
        max_length=7,
        choices=Difficult_CHOICES,
        default='EASY')
    users = models.ManyToManyField('Profile', through='UsersProblems')


class UsersProblems(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(SqlProblem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'problem']
