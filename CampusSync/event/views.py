from django.shortcuts import render
from rest_framework.response import Response
from .serializer import EventSerializer, AttendeesSerializer
from .models import Event
from user.models import Host
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer

from rest_framework import status


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


    def create(self, request, *args, **kwargs):
        # Check if 'host_id' is provided in the request data
        if 'host_id' not in request.data:
            return Response({"host_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get host_id from the request data
        host_id = request.data.get('host_id')

        # Validate if the host exists
        try:
            host_instance = Host.objects.get(pk=host_id)
        except Host.DoesNotExist:
            return Response({"host_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

        # Create the event object
        self.perform_create(serializer)

        # Add host object as a foreign key to the event
        # event_instance = self.get_object()
        event_instance = serializer.instance

        event_instance.host = host_instance
        event_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def order_by_recent(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    events = Event.objects.order_by("-date_posted")
    return Response(events.values())

@api_view(['GET'])
def order_by_old(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    events = Event.objects.order_by("date_posted")
    return Response(events.values())


@api_view(['GET'])
def order_by_upvote(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    events = Event.objects.order_by("-s")
    return Response(events.values())

@api_view(['GET'])
def order_by_downvote(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    events = Event.objects.order_by("-downvotes")
    return Response(events.values())


def custom_404(request, exception):
    print("$$")
    return render(request, 'event/404.html', status=404)



@api_view(['GET'])
def search(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
    if 'event_name' not in request.data:
        return Response({'error': 'Missing required field: event_name'}, status=status.HTTP_400_BAD_REQUEST)

    event_name = request.data['event_name']
    events = Event.objects.filter(name__icontains=event_name)

    if not events.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Return the list of events
    return Response(events.values()) 

class RSVPviewset(viewsets.ModelViewSet):
    serializer_class = AttendeesSerializer
    def get_queryset(self):
        e_id = self.kwargs['event_pk']
        return Event.objects.get(event=e_id).atendees.all()
    


