from django.shortcuts import render, HttpResponse

# Create your views here.
def get_events(request):
    return HttpResponse('Hi')