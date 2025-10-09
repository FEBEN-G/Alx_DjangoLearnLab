from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserProfileSerializer(read_only=True)
    target_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'verb', 'notification_type', 
            'target', 'timestamp', 'is_read', 'target_url'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_target_url(self, obj):
        """Generate URL for the target object if applicable"""
        if obj.target_content_type and obj.target_object_id:
            model_name = obj.target_content_type.model
            if model_name == 'post':
                return f"/api/posts/posts/{obj.target_object_id}/"
            elif model_name == 'comment':
                return f"/api/posts/comments/{obj.target_object_id}/"
        return None

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']

class NotificationCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField()
    total_count = serializers.IntegerField()