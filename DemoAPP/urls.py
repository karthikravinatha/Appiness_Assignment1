from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('student/', views.StudentViewset.as_view(), name='student'),
    path('student_list/', views.StudentListView.as_view(), name='student_list'),
]
