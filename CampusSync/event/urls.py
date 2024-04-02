from django.urls import path 
from . import views
from rest_framework.generics import ListCreateAPIView
from .models import Event
from .serializer import EventSerializer
from .views import EventViewSet
  
# urlpatterns = [ 
#     path('updateEvent/', views.update_event, name = 'update-event'), 
#     path('deleteEvent/', views.delete_event, name = 'delete-event'), 
#     path('events/', ListCreateAPIView.as_view(queryset=Event.objects.all(), serializer_class=EventSerializer), name='event-create-and-list')

# ]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
urlpatterns = router.urls

 
urlpatterns = [ 
    path('updateEvent/', views.update_event, name = 'update-event'), 
    path('deleteEvent/', views.delete_event, name = 'delete-event'), 
    path('events/', ListCreateAPIView.as_view(queryset=Event.objects.all(), serializer_class=EventSerializer), name='event-list')

]
