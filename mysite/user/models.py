from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 32)
    passwd = models.CharField(max_length = 32)
    nickname = models.CharField(max_length=64)
    create_date = models.DateTimeField()
