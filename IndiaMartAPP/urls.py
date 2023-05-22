from django.urls import include,path
from . import views


urlpatterns = [
    path('grabDoors/', views.GrabDoorsView.as_view())
]