# Created by Karthik Ravinatha at 9:13 am 25/05/23 using PyCharm
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', views.RelationsView.as_view(), name='relations')
]
