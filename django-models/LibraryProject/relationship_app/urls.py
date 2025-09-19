# relationship_app/urls.py
from django.urls import path
from . import views
from . import admin_view, librarian_view, member_view

urlpatterns = [
    # List and library detail
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Role-based
    path('admin-view/', admin_view.admin_view, name='admin_view'),
    path('librarian-view/', librarian_view.librarian_view, name='librarian_view'),
    path('member-view/', member_view.member_view, name='member_view'),

    # Book CRUD (secured with custom permissions)
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
]

