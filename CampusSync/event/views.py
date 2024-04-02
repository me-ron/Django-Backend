from .serializer import EventSerializer
from .models import Event
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
 
class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

