from django.db import models
from enum import Enum


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

    # class Meta:
    #    db_table = 'HR'


class ThirdProblem(models.Model):
    barcode = models.BigIntegerField(primary_key=True, unique=True, default=0, null=False)
    item_name = models.TextField(max_length=200, null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return f'{self.barcode, self.item_name, self.manufacturer, self.price}'

    class Meta:
        db_table = "db_items"


class ClothingItem(Enum):
    SHIRTS = 'Shirts'
    PANTS = 'Pants'
    TROUSERS = 'Trousers'
    SHOES = 'Shoes'
    SUITS = 'Suits'

    def get_values():
        return [ClothingItem.SHIRTS.value, ClothingItem.PANTS.value, ClothingItem.TROUSERS.value, ClothingItem.SHOES.value, ClothingItem.SUITS.value]


class FifthProblem(models.Model):
    barcode = models.BigIntegerField(primary_key=True, unique=True, default=0, null=False)
    item_name = models.TextField(max_length=200, null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return f'{self.barcode, self.item_name, self.manufacturer, self.price}'

    class Meta:
        db_table = 'db_clothing_store'

class SixthProblem(models.Model):
    answer = models.TextField(max_length=200, null=True)

    class Meta:
        db_table = "sixth_answer"