from rest_framework import serializers
from .models import Event
from user.models import Host



class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        # fields = ['id', 'name', 'description', 'event_date'
        #           , 'date_posted',  'poster', 'host', 'upvotes', 'downvotes', 'saved_by']

        fields = ['id']

class EventSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=Host.objects.all())
    class Meta:
        model = Event
        fields = '__all__'
