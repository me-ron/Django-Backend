from django.urls import path 
from . import views
from rest_framework.generics import ListCreateAPIView
from .models import Event
from .serializer import EventSerializer

  
urlpatterns = [ 
    path('updateEvent/', views.update_event, name = 'update-event'), 
    path('deleteEvent/', views.delete_event, name = 'delete-event'), 
    path('events/', ListCreateAPIView.as_view(queryset=Event.objects.all(), serializer_class=EventSerializer), name='event-list')

]