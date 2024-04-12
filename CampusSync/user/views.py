from .serializer import HostDetailSerializer, UserSerializer, HostSerializer
from .models import User, Host
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status

from event.serializer import EventSerializer

from rest_framework.decorators import api_view
 
class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # http_method_names = ['delete', ]




class HostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Host.objects.all()
    # http_method_names = ['delete', ]

    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return HostSerializer
        return HostDetailSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     self.perform_create(serializer)

    #     # Get the user_id from the request data
    #     user_id = request.data.get('user_id')

    #     # Call super().create() to properly perform creation

    #     # Add the user to the admins field of the host
    #     # host_instance = serializer.instance
    #     user_instance = User.objects.get(pk=user_id)
    #     # print(user_instance)
    #     # for user in user_instance:  # Assuming User model exists
    #     # host_instance.admins.set(user_instance)
        
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class JWTHome(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
 
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        h_id = self.kwargs['host_pk']
        return Host.objects.get(pk=h_id).events_hosted.all()
    

@api_view(['POST'])
def events_by_host(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'host_id' not in request.data:
            return Response({"host_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)


    host_id = request.data['host_id']
    host = Host.objects.get(pk=host_id)
    events = host.events_hosted.all()
    return Response(events.values())

@api_view(['POST'])
def hosts_under_user(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'user_id' not in request.data:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"user_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

    hosts = user.hosts_owned.all()
    return Response(hosts.values())



@api_view(['POST'])
def user_following(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'user_id' not in request.data:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"user_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

    followings = user.following.all()
    return Response(followings.values())

@api_view(['POST'])
def follow_host(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'user_id' not in request.data:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    elif 'host_id' not in request.data:
            return Response({"host_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']
    host_id = request.data['host_id']

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"user_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

    try:
        host = Host.objects.get(pk=host_id)
    except Host.DoesNotExist:
        return Response({"host_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)


    if user in host.followers.all():
        host.followers.remove(user)
        
        host.notifications -= 1

        host.save()

        serializer = UserSerializer(host.followers.all(), many=True)

        return Response({'success': 'Your follow is removed from this host'
                            ,'followers': serializer.data})
    

    host.followers.add(user)
    host.notifications += 1
    host.save()

    serializer = UserSerializer(host.followers.all(), many=True)

    return Response({'success': 'Your follow is added to this host'
                            ,'followers': serializer.data})
    



@api_view(['POST'])
def events_rsvpd(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'user_id' not in request.data:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"user_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

    events_rsvpd = user.events_attending.all()
    serializer = EventSerializer(events_rsvpd, many=True)
    print("FG")
    return Response(serializer.data)



@api_view(['POST'])
def questions_by_user(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if 'user_id' not in request.data:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data['user_id']

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"user_id": ["Invalid host ID."]}, status=status.HTTP_400_BAD_REQUEST)

    questions = user.questions.all()
    return Response(questions.values())
