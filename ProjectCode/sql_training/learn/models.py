from django.db import models


class DummyUser(models.Model):
    username = models.TextField(primary_key=True, max_length=200, null=False)
    password = models.TextField(max_length=200, null=False)

    class Meta:
        db_table = 'db_dummy_users'
