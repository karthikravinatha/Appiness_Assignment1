from django.db import models


# Create your models here.
class AuthorModels(models.Model):
    author_name = models.CharField(max_length=124, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "author"


class BookModel(models.Model):
    book_name = models.CharField(max_length=124)
    author = models.ForeignKey(AuthorModels, related_name='book',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "book"
