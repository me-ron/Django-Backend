from django.urls import path 
from . import views
  
urlpatterns = [ 
    path('', views.display_events, name='display_events'), 
    path('vote/<str:event_id>/', views.vote_event, name = "vote"),
    path('showDetail/<str:event_id>', views.show_detail, name = "showDetail"),
    path('search/', views.search_event, name = 'search-event'), 
    path('filter/', views.filter_event, name = 'filter-event'), 
    path('createEvent/', views.create_event, name = 'create-event'), 
    path('deleteEvent/', views.delete_event, name = 'delete-event'), 
]