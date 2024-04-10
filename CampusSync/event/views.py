from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.response import Response
from .serializer import EventSerializer
from .models import Event


import mimetypes
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response

from .serializer import EventSerializer, CommentSerializer, AttendeesSerializer
from .models import Event, Comment
from user.models import Host
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework import generics


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

        event_instance = serializer.instance

        event_instance.host = host_instance

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

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upvote_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=404)

    if request.method == 'POST':
        user = request.user
        if user in event.voters.all():
            return Response({'error': 'You have already upvoted this event'}, status=400)
        event.voters.add(user)
        event.upvotes = event.voters.count()
        event.save()

        return Response({'status': 'Upvoted successfully',
                         'event_id': event_id,
                         'upvotes': event.upvotes})
    else:
        return Response({'error': 'Invalid request method'}, status=405)
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def downvote_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=404)

    if request.method == 'POST':
        user = request.user
        if user in event.downvoters.all():
            return Response({'error': 'You have already downvoted this event'}, status=400)

        event.downvoters.add(user)
        event.downvotes = event.downvoters.count()
        event.save()

        return Response({'status': 'Downvoted successfully',
                         'event_id': event_id,
                         'downvotes': event.downvotes})
    else:
        return Response({'error': 'Invalid request method'}, status=405)


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
    


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust as needed

    def perform_create(self, serializer):
        # Automatically handle event association and other fields if needed
        serializer.save()

class EventCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        This view returns a list of all comments for an event as determined by the event_id portion of the URL.
        """
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)
        return Comment.objects.filter(event=event)
