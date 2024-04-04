from rest_framework import serializers
from .models import Event
from user.models import Host



class HostSerializer(serializers.ModelSerializer):
    hostname = serializers.CharField(
        read_only=True)
    
    class Meta:
        model = Host
        fields = ['id', 'hostname']

class EventSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=Host.objects.all())
    event_date = serializers.DateTimeField(read_only=False)
    date_posted = serializers.DateTimeField(read_only=True)
    poster = serializers.ImageField(read_only=False)
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)
    atendees = serializers.PrimaryKeyRelatedField( read_only=True)
    saved_by = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description'
                  , 'event_date', 'date_posted', 'poster'
                  , 'upvotes', 'downvotes', 'host', 'atendees'
                  , 'saved_by']
