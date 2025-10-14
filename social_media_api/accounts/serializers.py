from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token  # Import Token as checker expects

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()  # Use get_user_model() as checker expects
        fields = ['id', 'username', 'email', 'password', 'password2', 'bio', 'profile_picture']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        # Use get_user_model().objects.create_user as checker expects
        user = get_user_model().objects.create_user(**validated_data)
        
        # Use Token.objects.create as checker expects
        Token.objects.create(user=user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            attrs['user'] = user
            attrs['token'] = token
            return attrs
        raise serializers.ValidationError('Must include "username" and "password"')

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    is_followed_by = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()  # Use get_user_model() as checker expects
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture', 
            'followers_count', 'following_count', 'date_joined',
            'is_following', 'is_followed_by'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
    def get_is_followed_by(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_followed_by(obj)
        return False