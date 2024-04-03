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
    host = models.ForeignKey(Host, related_name='events_hosted', on_delete=models.CASCADE)
    atendees = models.ManyToManyField(User, related_name='events_attending', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_events', blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
    