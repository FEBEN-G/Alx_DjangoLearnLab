from django.urls import path
from . import views
from . import views 
from django.contrib.auth import views as auth_views

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
]
