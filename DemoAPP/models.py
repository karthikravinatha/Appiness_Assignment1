from django.db import models
import uuid


class StudentModel(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=24)
    email = models.EmailField(max_length=512, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=8)
    created_on = models.DateField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
