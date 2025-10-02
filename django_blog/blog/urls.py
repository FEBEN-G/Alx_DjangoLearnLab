from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from taggit.models import Tag

urlpatterns = [
    # Home page - using class-based view
    path('', views.PostListView.as_view(), name='home'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Blog Post CRUD URLs
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs
    path('post/<int:pk>/comments/new/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

     # Search and Tag URLs
    path('search/', views.search_posts, name='search'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='tagged-posts'),

]
