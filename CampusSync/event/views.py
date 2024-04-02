from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404, JsonResponse
from user.models import Host
from .serializer import EventSerializer
from .models import Event
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def delete_event(request):
    event_id = request.data['id']
    event = Event.objects.filter(pk=int(event_id))
    if event:
        # event.delete()
        return JsonResponse({'status': 'succ'})
    return JsonResponse({'status': 'Err'})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def update_event(request):

    event = Event.objects.get(pk=int(request.data['id']))
    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse( {'events': "succ"} )
    return Response(serializer.errors)
    

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ['name', 'description', 'host__hostname',]
    search_fields = ['name', 'description', 'host__hostname',]
    # ordering_fields = ['date_created']
    ordering = ['name']

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, validated_data):
        event_data = validated_data.pop('host')
        host = Host.objects.create(**validated_data)
        Host.objects.create(host=host, **event_data)
        return host
    
 