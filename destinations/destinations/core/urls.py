from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='/'),
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('users/new/', views.create_user, name='create_user'),
    path('sessions/', views.sessions, name='sessions'),
    path('sessions/new/', views.create_session, name='create_session'),
    path('sessions/destroy/', views.destroy_session, name='destroy_session'),
    path('destinations/new/', views.create_destination, name='create_destination'),
    path('destinations/', views.destinations, name='destinations'),
    path('destinations/<int:destination_id>/', views.edit_destination, name='edit_destination'),
    path('destinations/<int:destination_id>/delete/', views.delete_destination, name='delete_destination'),
]