from rest_framework import serializers
from .models import User, Host
from event.models import Event
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        # ...

        return token

class HostSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        read_only=True,
        )
    # user_id = serializers.IntegerField(write_only=True)
    description = serializers.CharField(required=True)
    account_pic = serializers.ImageField(required=False, read_only=False)    
    admins = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, many=True)
    # followers = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, many=True)
    notifications = serializers.IntegerField(
        read_only=True,
        )

    class Meta:
        model = Host 
        fields = ['id', 'hostname', 'description', 'account_pic'
                  , 'admins', 'followers', 'notifications']
    
    
    # def create(self, validated_data):
    #     # user_id = validated_data.pop('user_id')
    #     print(validated_data)
    #     # host = Host.objects.create(**validated_data)
    
    #     # host = Host.objects.get(hostname=validated_data['hostname'])
    #     # Assuming 'admins' is the many-to-many field in Host model
    #     # user_instance = User.objects.get(pk=user_id)  # Assuming User model exists
    #     # host
    #     # host.admins.set(user_instance)
        
    #     return Host.objects.get(pk=1)
        
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


    id = serializers.IntegerField(
        read_only=True,
        )
    notifications = serializers.IntegerField(
        read_only=True,
        )
    
    profile_pic = serializers.ImageField(required=False, read_only=False)    


    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'profile_pic', 'notifications']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['id', 'name', 'description', 'event_date',
#                   'date_posted', 'poster', 'upvotes', 'downvotes', 'address']


class HostDetailSerializer(serializers.ModelSerializer):
    admins = UserSerializer(many = True)
    followers = UserSerializer(many = True)
    account_pic = serializers.ImageField(required=False, read_only=False)    

    class Meta:
        model = Host 
        fields = ['id', 'hostname', 'description', 'account_pic'
                  , 'admins', 'followers', 'notifications']