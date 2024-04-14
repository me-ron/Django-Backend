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
from user.serializer import HostSerializer
from .models import Event, Comment
from user.models import Host, User
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
# from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework import generics

from rest_framework import filters



class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)


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
    return render(request, 'event/404.html', status=404)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upvote_event(request, event_id):

    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=404)

    if request.method == 'POST':
        if 'user_id' not in request.data or not request.data['user_id']:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(pk=request.data['user_id'])


        if user in event.downvoters.all():
            event.downvoters.remove(user)
            event.downvotes = event.downvoters.count()
            
            user.notifications -= 1
            event.notifications -= 1

        if user in event.upvoters.all():
            event.upvoters.remove(user)
            event.upvotes = event.upvoters.count()
            user.notifications -= 1
            event.notifications -= 1

            event.save()

            return Response({'success': 'Your upvote is removed from this event'
                             ,'event_id': event_id
                            ,'upvotes': event.upvotes})
        

        event.upvoters.add(user)
        event.upvotes = event.upvoters.count()
        event.notifications += 1
        user.notifications += 1


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
        if 'user_id' not in request.data or not request.data['user_id']:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=request.data['user_id'])

        if user in event.upvoters.all():
            event.upvoters.remove(user)
            event.upvotes = event.upvoters.count()
            
            user.notifications -= 1
            event.notifications -= 1


        if user in event.downvoters.all():
            event.downvoters.remove(user)
            event.downvotes = event.downvoters.count()
            
            user.notifications -= 1
            event.notifications -= 1

            event.save()

            return Response({'success': 'Your downvote is removed from this event'
                             ,'event_id': event_id
                            ,'downvotes': event.downvotes})

        event.downvoters.add(user)
        event.downvotes = event.downvoters.count()
        event.notifications += 1
        user.notifications += 1


        event.save()

        return Response({'status': 'Downvoted successfully',
                         'event_id': event_id,
                         'downvotes': event.downvotes})
    else:
        return Response({'error': 'Invalid request method'}, status=405)



class RSVPviewset(viewsets.ModelViewSet):
    serializer_class = AttendeesSerializer
    def get_queryset(self):
        e_id = self.kwargs['event_pk']
        # return User.objects.filter(events_attending = e_id)
        print("DDDD")
        return Event.objects.get(pk=e_id).atendees.all()
    
    def create(self, request, event_pk):
        e_id = self.kwargs['event_pk']
        # e_id = request.data['e_id']
        if 'id' not in request.data:
            return Response({"id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event_instance = Event.objects.get(pk=e_id)
        except Host.DoesNotExist:
            return Response({"event_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('id')

        event_instance.atendees.add(User.objects.get(pk=user_id))
        
        event_instance.notifications += 1
        event_instance.save()

        serializer = EventSerializer(event_instance)

        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust as needed

    def perform_create(self, serializer):
        # Automatically handle event association and other fields if needed
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.instance.commentor)
        event = serializer.validated_data.get('event')
        # print(event.comments)
        # comments = Comment.objects.filter(event=event).order_by("-date_posted")
        comments = event.comments.all()
        # print(comments)
        # Modify the serializer class if needed to include many=True
        comments_serializer = CommentSerializer(comments, many=True)
        
        return Response(comments_serializer.data, status=status.HTTP_201_CREATED)

class EventCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        This view returns a list of all comments for an event as determined by the event_id portion of the URL.
        """
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)
        print(event.comments.all())
        return event.comments.all()
        # return Comment.objects.filter(event=event)