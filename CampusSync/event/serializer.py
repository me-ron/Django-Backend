from rest_framework import serializers

from .models import Event, Comment
from user.models import Host, User

from user.serializer import HostSerializer

from user.serializer import UserSerializer

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
    address = serializers.CharField(required=True)

    #atendees = serializers.PrimaryKeyRelatedField( read_only=True)
    host = HostSerializer(required=False, read_only=True)
    # atendees = serializers.PrimaryKeyRelatedField( read_only=True)

    #atendees = serializers.PrimaryKeyRelatedField( read_only=True)
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
        fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    commentor = UserSerializer(read_only=True)
    commentor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='commentor', write_only=True)
    # author = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Comment
        # fields = ['id', 'content', 'upvotes', 'date_posted', 'event', 'commentor']
        fields = '__all__'
        read_only_fields = ('id', 'date_posted', 'upvotes', 'downvotes')

    def create(self, validated_data):
        # Assuming `event` is provided in the request to link the comment
        event = validated_data.pop('event', None)
        if event:
            # comment = Comment.objects.create(event=event, **validated_data)
            comments = Comment.objects.filter(event = event)
            return comments
        else:
            raise serializers.ValidationError({'event': 'Event ID is required'})

