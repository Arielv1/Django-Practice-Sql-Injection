from enum import Enum

from django.db import models



class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class InjectionTypes(Enum):
    IN_BAND = "In-band"
    UNION = "Union Based"
    BLIND = "Blind"


class ProblemsContentTable(models.Model):
    difficulty = models.CharField(max_length=200, null=True)
    hreference = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.difficulty} {self.hreference} {self.name} {self.type} {self.solved}"

    class Meta:
        db_table = 'db_problems_content_table'
