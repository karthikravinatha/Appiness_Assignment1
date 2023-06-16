from django.db import models


# Create your models here.

class UserModel(models.Model):
    first_name = models.CharField(max_length=512)
    dob = models.DateField()
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "user"


class UserAddress(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.PROTECT)
    address = models.CharField(max_length=512)
    street = models.CharField(max_length=124)
    pincode = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "user_address"
