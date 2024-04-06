from django.shortcuts import render
from rest_framework.response import Response
from .serializer import EventSerializer
from .models import Event
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@api_view(['GET','POST']) 
def event_notifications(request):
    print(request.data)
    event_id = request.data['event_id']
    event = Event.objects.filter(pk=event_id)

    if request.method == 'GET' and event:
        return Response({'status': 'succesful get',
                        'event_id': str(event_id),
                        'event_notifications': str(event.notifications)})
    
    elif request.method == 'POST' and event:
        change = request.data[change]
        event.notifications = event.notifications + int(change)
        event.save()

        return Response({'status': 'succesful post',
                        'event_id': str(event_id),
                        'event_notifications': str(event.notifications)})
    
    return Response({'status': 'Failed, no such event'})


def custom_404(request, exception):
    print("$$")
    return render(request, 'event/404.html', status=404)