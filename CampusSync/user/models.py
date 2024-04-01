from django.db import models
# from event.models import Event
# Create your models here.

class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    block = models.IntegerField(null=True, blank=True)
    office = models.IntegerField(null=True, blank=True)
    phone_num = models.CharField(null=True, blank=True, max_length=13)
    #AdressObj.host -> host

    def __str__(self) -> str:
        return f"{self.id}"

class Host(models.Model):
    id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=500)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    account_pic = models.ImageField(upload_to='_user/host_profile_pics', default='_user/defaults/default_account.png', null=True, blank=True)
    # followers -> dataset from User.following
    #events -> backref from Event.host ,, HostObj.event_set.all() -> all events
    #-> one-to-one with Adress 
    host_address = models.OneToOneField(Address, on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.hostname}"


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    profile_pic = models.ImageField(upload_to='_user/user_profile_pics', default='_user/defaults/default_profile.png', null=True, blank=True)
    # -> many-to-many with Event
    # events_saved = models.ManyToManyField(Event) 
    # events_reserved -> dataset to Event.atendees ,, UserObj.event_set.all() -> events_reserved
    # questions_asked->dataset from Question ,, UserObj.question_set.all() -> questions_asked
    # questions_answered->dataset from Answer ,, UserObj.answer_set.all() -> answers given
    #  -> many-to-many with Host
    following = models.ManyToManyField(Host, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"
