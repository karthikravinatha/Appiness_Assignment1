# Created by Karthik Ravinatha at 2:49 pm 16/06/23 using PyCharm
from django.urls import path
from . import views

urlpatterns = [
    path("", views.AuthorViews.as_view(), name="foreign_key_reln"),
    path("book", views.BookViews.as_view(), name="foreign_key_reln")
]
