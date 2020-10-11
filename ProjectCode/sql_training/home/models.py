from enum import Enum

from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.


def _generate_unique_id():
    return uuid.uuid4()


class Customer(models.Model):
    username = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now=True)
    customer_id = _generate_unique_id()

    def __str__(self):
        return f'{self.username, self.email, self.date_created, self.customer_id}'


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class InjectionTypes(Enum):
    IN_BAND = "In-band"
    UNION = "Union Based"
    BLIND = "Blind"


class ProblemReference(models.Model):
    # problem_id = _generate_unique_id()
    # difficulty = models.IntegerField(max_length=200, null=True)

    def __init__(self, difficulty, details, type, ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.problem_id = _generate_unique_id()
        self.difficulty = difficulty if difficulty is Difficulty.EASY or Difficulty.MEDIUM or Difficulty.HARD else None
        self.details = details
        self.ref = ref
        self.type = type

    def __str__(self):
        return f'{self.problem_id, self.difficulty, self.details, self.ref, self.type}'
