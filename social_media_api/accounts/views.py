from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# CORRECTED: Follow/Unfollow views using GenericAPIView with proper methods
class FollowUserView(generics.GenericAPIView):
    """
    View for following a user using GenericAPIView
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        if target_user == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following
        if target_user not in request.user.following.all():
            request.user.following.add(target_user)
            return Response({
                'detail': f'You are now following {target_user.username}.',
                'is_following': True,
                'followers_count': target_user.followers.count(),
                'following_count': request.user.following.count()
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': f'You are already following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UnfollowUserView(generics.GenericAPIView):
    """
    View for unfollowing a user using GenericAPIView
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        # Remove from following
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)
            return Response({
                'detail': f'You have unfollowed {target_user.username}.',
                'is_following': False,
                'followers_count': target_user.followers.count(),
                'following_count': request.user.following.count()
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': f'You are not following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        if target_user == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if target_user not in request.user.following.all():
            request.user.following.add(target_user)
            return Response({
                'detail': f'You are now following {target_user.username}.',
                'is_following': True,
                'followers_count': target_user.followers.count(),
                'following_count': request.user.following.count()
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': f'You are already following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)
            return Response({
                'detail': f'You have unfollowed {target_user.username}.',
                'is_following': False,
                'followers_count': target_user.followers.count(),
                'following_count': request.user.following.count()
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': f'You are not following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class FollowStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        
        return Response({
            'is_following': request.user.following.filter(id=target_user.id).exists(),
            'is_followed_by': target_user.following.filter(id=request.user.id).exists(),
            'followers_count': target_user.followers.count(),
            'following_count': target_user.following.count()
        })

class UserFollowersView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return user.followers.all()

class UserFollowingView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return user.following.all()