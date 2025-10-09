from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Notification
from .serializers import (
    NotificationSerializer, 
    NotificationUpdateSerializer,
    NotificationCountSerializer
)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        unread_notifications = self.get_queryset().filter(is_read=False)
        page = self.paginate_queryset(unread_notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({
            'detail': f'Marked {updated_count} notifications as read.',
            'updated_count': updated_count
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'detail': 'Notification marked as read.'})
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Mark a specific notification as unread"""
        notification = self.get_object()
        notification.mark_as_unread()
        return Response({'detail': 'Notification marked as unread.'})

class NotificationCountView(APIView):
    """
    Get notification counts for the current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
        total_count = Notification.objects.filter(recipient=request.user).count()
        
        serializer = NotificationCountSerializer({
            'unread_count': unread_count,
            'total_count': total_count
        })
        return Response(serializer.data)