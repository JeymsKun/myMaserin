from django.urls import path
from . import views

urlpatterns = [
    path('', views.nba_list, name='nba_list'),
]