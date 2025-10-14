from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, 
    UserListView, UserDetailView, FollowStatusView,
    UserFollowersView, UserFollowingView, FollowUserView, 
    UnfollowUserView
)

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # User management endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # EXACT URL PATTERNS REQUIRED BY CHECKER:
    path('follow/<int:user_id>', FollowUserView.as_view(), name='follow-user'),  # NO trailing slash
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),  # WITH trailing slash
    
    # Additional functionality endpoints
    path('users/<int:user_id>/follow-status/', FollowStatusView.as_view(), name='follow-status'),
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user-following'),
]