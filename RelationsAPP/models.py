from django.db import models


class RelationsHeaderModel(models.Model):
    invoice_type = models.IntegerField()
    invoice_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()

    # class Meta:
    #     db_table = "Invoice_Header"


class RelationsDetailModel(models.Model):
    invoice_header_id = models.ForeignKey('RelationsHeaderModel', on_delete=models.CASCADE)
    category_id = models.PositiveIntegerField()
    quantity = models.FloatField()
    uom = models.PositiveIntegerField()
    price = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    objects = models.Manager()



