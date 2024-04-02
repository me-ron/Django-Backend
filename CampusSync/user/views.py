from .serializer import UserSerializer
from .models import User
# from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
 
class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Events.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
