from django.http import JsonResponse
# from django.shortcuts import render, HttpResponse
from .serializer import EventSerializer
from .models import Event
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return JsonResponse( {'events': serializer.data} )
