# Created by Karthik Ravinatha at 12:13 pm 16/06/23 using PyCharm
from django.urls import path
from . import views

urlpatterns = [
    path('', views.OneToOneViews.as_view(), name="one_to_one_app")
]
