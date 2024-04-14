from django.db import models
from user.models import Host, User
# from forum.models import EventForum

# Create your models here.
class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200) 
    description = models.TextField(default="Default description")
    event_date = models.DateTimeField()
    date_posted = models.DateTimeField(auto_now_add=True)
    poster = models.ImageField(upload_to='_event/posters', default='_event/defaults/default_poster.png', null=True, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes  = models.IntegerField(default=0)
    upvoters = models.ManyToManyField(User, related_name='upvote_events')
    downvoters = models.ManyToManyField(User, related_name='downvote_events')
    host = models.ForeignKey(Host, related_name='events_hosted',null=True, blank=True, on_delete=models.CASCADE)
    atendees = models.ManyToManyField(User, related_name='events_attending', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_events', blank=True)
    notifications = models.IntegerField(default=0)
    address = models.CharField(max_length=200) 

    def __str__(self) -> str:
        return f"{self.name}"
    

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes  = models.IntegerField(default=0)
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)    
    commentor = models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.id}"