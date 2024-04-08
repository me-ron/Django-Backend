from rest_framework import serializers
from .models import Event, Comment
from user.models import Host



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
        fields = ['id', 'host_id', 'name', 'description', 'event_date'
                  ,'date_posted', 'poster', 'upvotes', 'downvotes']

    def create(self, validated_data):
        # Remove 'host_id' from validated_data since it's not a field of Event model
        host_id = validated_data.pop('host_id')

        # Create event object
        event = Event.objects.create(**validated_data)

        # Assuming 'host' is the foreign key field in Event model
        host_instance = Host.objects.get(pk=host_id)
        event.host = host_instance
        # event.save()
        
        return event
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'upvotes', 'date_posted', 'event']
        read_only_fields = ('id', 'date_posted', 'upvotes', 'downvotes')

    def create(self, validated_data):
        # Assuming `event` is provided in the request to link the comment
        event = validated_data.pop('event', None)
        if event:
            # try:
            #     event = Event.objects.get(id=event_id)
            # except Event.DoesNotExist:
            #     raise serializers.ValidationError({'event': 'Invalid event ID'})
            comment = Comment.objects.create(event=event, **validated_data)
            return comment
        else:
            raise serializers.ValidationError({'event': 'Event ID is required'})