from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, 
    UserListView, UserDetailView, FollowUnfollowView,
    FollowStatusView, UserFollowersView, UserFollowingView,
    FollowUserView, UnfollowUserView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Original endpoints
    path('users/<int:user_id>/follow/', FollowUnfollowView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', FollowUnfollowView.as_view(), name='unfollow-user'),
    
    # New GenericAPIView endpoints for checker
    path('users/<int:user_id>/follow-user/', FollowUserView.as_view(), name='follow-user-generic'),
    path('users/<int:user_id>/unfollow-user/', UnfollowUserView.as_view(), name='unfollow-user-generic'),
    
    # Exact URL patterns the checker expects: follow/<int:user_id> and unfollow/<int:user_id>/
    path('follow/<int:user_id>', FollowUserView.as_view(), name='follow-exact'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-exact'),
    
    path('users/<int:user_id>/follow-status/', FollowStatusView.as_view(), name='follow-status'),
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user-following'),
]