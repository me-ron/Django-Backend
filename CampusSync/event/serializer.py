from rest_framework import serializers
from .models import Event
from user.models import Host, User




class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        )
    # host = serializers.PrimaryKeyRelatedField(queryset=Host.objects.all())
    host_id = serializers.IntegerField(write_only=True)

    event_date = serializers.DateTimeField(read_only=False)
    date_posted = serializers.DateTimeField(read_only=True)
    poster = serializers.ImageField(read_only=False, required=False)
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)
    # atendees = serializers.PrimaryKeyRelatedField( read_only=True)
    # saved_by = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'host_id', 'host', 'name', 'description', 'event_date'
                  ,'date_posted', 'poster', 'upvotes', 'downvotes', 'address']

    def create(self, validated_data):
        # Remove 'host_id' from validated_data since it's not a field of Event model
        host_id = validated_data.pop('host_id')

        # Create event object
        event = Event.objects.create(**validated_data)

        # Assuming 'host' is the foreign key field in Event model
        host_instance = Host.objects.get(pk=host_id)
        event.host = host_instance
        event.save()
        
        return event
    
class AttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email','profile_pic']