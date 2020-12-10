from django.db import models
from enum import Enum


# Create your models here.
class CheckProblems(models.Model):
    username = models.CharField(max_length=200, null=True)
    problemnumber = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now=True)


class Employee(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True, default=0, null=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.id, self.first_name, self.last_name, self.age}'

    class Meta:
        db_table = 'db_employees'


class ClothingItem(Enum):
    SHIRTS = 'Shirts'
    PANTS = 'Pants'
    TROUSERS = 'Trousers'
    SHOES = 'Shoes'
    SUITS = 'Suits'

    def get_values():
        return [ClothingItem.SHIRTS.value, ClothingItem.PANTS.value, ClothingItem.TROUSERS.value,
                ClothingItem.SHOES.value, ClothingItem.SUITS.value]


class ClothingStore(models.Model):
    barcode = models.BigIntegerField(primary_key=True, unique=True, default=0, null=False)
    item_name = models.TextField(max_length=200, null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return f'{self.barcode, self.item_name, self.manufacturer, self.price}'

    class Meta:
        db_table = 'db_clothing_shop'


class Vehicle(models.Model):
    car_id = models.CharField(max_length=200, null=False, primary_key=True)
    num_wheels = models.IntegerField(null=True)
    manufacturer = models.CharField(max_length=200, null=True)
    num_of_accidents = models.IntegerField(null=True)
    total_km = models.FloatField(null=True)
    is_automatic = models.BooleanField(null=False, default=True)

    class Meta:
        db_table = 'db_vehicles'


class BlindSecret(models.Model):
    secret = models.TextField(max_length=200, null=True)

    class Meta:
        db_table = 'db_secret'


class Safe(models.Model):
    secret_pass = models.CharField(max_length=200, null=True)
    prize = models.IntegerField(null=True)

    class Meta:
        db_table = 'secret_safe'


class User(models.Model):
    username = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'db_users'

class UserRole(Enum):
    USER = 'User'
    MANAGER = 'Manager'
    ADMIN = 'Admin'