from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<uuid:event_id>/', views.event_detail, name='event_detail'),
    path('trainer/<uuid:trainer_id>/', views.trainer_detail, name='trainer_detail'),

    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<uuid:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<uuid:event_id>/delete/', views.event_delete, name='event_delete'),
]