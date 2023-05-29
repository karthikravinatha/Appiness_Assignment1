# Created by Karthik Ravinatha at 11:03 am 26/05/23 using PyCharm
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PdfParserViews.as_view(), name='pdfParser')
]
