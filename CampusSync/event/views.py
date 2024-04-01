from django.shortcuts import render, HttpResponse, redirect
from .models import Event

# Create your views here.

def create_event(request):
    # Accepting the informations from the form and adding it to the database
    return redirect('')

def delete_event(request):
    # This is the part where the host can control the event 
    return redirect('')

def update_event(request):
    #Again another crud operation
    return redirect('')

def display_events(request):
    events = Event.objects.all()
    context = {"events" : events}
    return render(request, "event/home.html", context)

def vote_event(request, event_id):
    # Write the vote logic here
    return redirect('')

def show_detail(request, event_id):
    # When a user click on the event this function will direct the user to the event detail page
    context = {"event_id" : event_id}
    return render(request, "event/home.html", context)


def search_event(request):
    # Here we are going to have a searched value with POST method to filter the objects by event name
    searched = ""
    events = Event.objects.filter(name__contains = searched)
    context = {"events" : events}
    return render(request, "event/home.html", context)

def filter_event(request):
    # Again here the variable by holds the post value from the filter buttons
    by = ""
    if by == "upvote": # assuming the button value is upvote
        events = Event.objects.order_by('-upvotes')
    elif by == "recent":
        events = Event.objects.order_by('-timestamp')
    else:
         events = Event.objects.all()

    context = {"events" : events}
    return render(request, "event/home.html", context)


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
