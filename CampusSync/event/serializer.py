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
    poster = serializers.ImageField(required=False, read_only=False)    

    # atendees = serializers.PrimaryKeyRelatedField( read_only=True)

    #atendees = serializers.PrimaryKeyRelatedField( read_only=True)
    # saved_by = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'host_id', 'host', 'name', 'description', 'event_date'
                  ,'date_posted', 'poster', 'upvotes', 'downvotes', 'address']

    # def create(self, validated_data):
    #     host_id = validated_data.pop('host_id')

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')  # Assuming user_id is provided in the request data
        try:
            host_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(host=host_user)
   

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

