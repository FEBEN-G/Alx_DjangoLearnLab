from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self and user not in self.following.all():
            self.following.add(user)
            # Create follow notification
            self._create_follow_notification(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user in self.following.all():
            self.following.remove(user)
            return True
        return False
    
    def is_following(self, user):
        """Check if the current user is following the given user"""
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        """Check if the current user is followed by the given user"""
        return self.followers.filter(id=user.id).exists()
    
    def _create_follow_notification(self, user):
        """Create follow notification"""
        try:
            from notifications.models import Notification
            Notification.create_follow_notification(recipient=user, actor=self)
        except:
            # Notifications app might not be ready during migration
            pass
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def get_feed_posts(self):
        """Get posts from users that the current user follows"""
        from posts.models import Post
        following_ids = self.following.values_list('id', flat=True)
        # Include user's own posts in the feed
        following_ids = list(following_ids) + [self.id]
        return Post.objects.filter(author_id__in=following_ids).order_by('-created_at')
    
    def get_unread_notifications_count(self):
        """Get count of unread notifications"""
        try:
            from notifications.models import Notification
            return Notification.objects.filter(recipient=self, is_read=False).count()
        except:
            return 0