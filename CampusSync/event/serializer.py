from rest_framework import serializers
from .models import Event
from user.models import Host



class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        )
    host = serializers.PrimaryKeyRelatedField(queryset=Host.objects.all())
    event_date = serializers.DateTimeField(read_only=False)
    date_posted = serializers.DateTimeField(read_only=True)
    poster = serializers.ImageField(read_only=False, required=False)
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)
    # atendees = serializers.PrimaryKeyRelatedField( read_only=True)
    # saved_by = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = Event
        fields = '__all__'