from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=UserProfileSerializer.Meta.model.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=UserProfileSerializer.Meta.model.objects.all(),
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_id', 'title', 'content', 
            'created_at', 'updated_at', 'comments', 'likes',
            'likes_count', 'comments_count', 'is_liked'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)