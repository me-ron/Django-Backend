from .serializer import UserSerializer, HostSerializer, EventSerializer
from .models import User, Host
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status

 
class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class HostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the user_id from the request data
        user_id = request.data.get('user_id')

        # Call super().create() to properly perform creation
        self.perform_create(serializer)

        # Add the user to the admins field of the host
        host_instance = serializer.instance
        user_instance = User.objects.get(pk=user_id)  # Assuming User model exists
        host_instance.admins.add(user_instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        return Host.objects.get(host=h_id).events_hosted.all()