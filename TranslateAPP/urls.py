# Created by Karthik Ravinatha at 4:03 pm 31/05/23 using PyCharm
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Translate.as_view())
]
