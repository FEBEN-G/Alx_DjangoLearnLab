from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('mention', 'Mention'),
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Generic Foreign Key for the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.actor} {self.verb} - {self.recipient}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def mark_as_unread(self):
        self.is_read = False
        self.save()
    
    @classmethod
    def create_follow_notification(cls, recipient, actor):
        """Create a follow notification"""
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='started following you',
            notification_type='follow'
        )
    
    @classmethod
    def create_like_notification(cls, recipient, actor, target):
        """Create a like notification"""
        content_type = ContentType.objects.get_for_model(target)
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='liked your post',
            notification_type='like',
            target_content_type=content_type,
            target_object_id=target.id
        )
    
    @classmethod
    def create_comment_notification(cls, recipient, actor, target):
        """Create a comment notification"""
        content_type = ContentType.objects.get_for_model(target)
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb='commented on your post',
            notification_type='comment',
            target_content_type=content_type,
            target_object_id=target.id
        )