from django.db import models


# Create your models here.
class DoorsHeaderModel(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=512)
    url = models.CharField(max_length=1024)
    created_on = models.DateField(auto_now=True)
    updated_on = models.DateField(auto_now_add=True)
    objects = models.Manager()


class DoorsDetailModel(models.Model):
    id = models.IntegerField(primary_key=True)
    header_id = models.IntegerField()
    sub_category_name = models.CharField(max_length=512)
    price = models.CharField(max_length=512)
    seller_name = models.CharField(max_length=512)
    seller_description = models.CharField(max_length=512)
    seller_rating = models.CharField(max_length=512)
    created_on = models.DateField(auto_now=True)
    updated_on = models.DateField(auto_now_add=True)
    objects = models.Manager()

