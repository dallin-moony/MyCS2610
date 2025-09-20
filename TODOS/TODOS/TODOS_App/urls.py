from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index_alt'),
    path('create/', views.create_todo, name='create_todo'),
]