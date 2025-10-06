from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import DatabaseError
from .models import Book
from .forms import BookForm  # Import our secure form

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books. Requires 'can_view' permission.
    Uses safe ORM queries to prevent SQL injection.
    """
    try:
        # Safe ORM query - no raw SQL to prevent SQL injection
        books = Book.objects.select_related('created_by').all()
        context = {
            'books': books,
            'can_create': request.user.has_perm('bookshelf.can_create'),
            'can_edit': request.user.has_perm('bookshelf.can_edit'),
            'can_delete': request.user.has_perm('bookshelf.can_delete'),
        }
        return render(request, 'bookshelf/book_list.html', context)
    except DatabaseError as e:
        # Log the error and show user-friendly message
        messages.error(request, 'Database error occurred. Please try again later.')
        return render(request, 'bookshelf/book_list.html', {'books': []})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book. Requires 'can_create' permission.
    Uses secure form handling to prevent XSS and other attacks.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                # Create book object without saving yet
                book = form.save(commit=False)
                # Set the created_by field to current user
                book.created_by = request.user
                # Save to database
                book.save()
                
                messages.success(request, f'Book "{book.title}" created successfully!')
                return redirect('bookshelf:book_list')
                
            except DatabaseError as e:
                messages.error(request, 'Database error occurred. Please try again.')
            except Exception as e:
                messages.error(request, f'Error creating book: {str(e)}')
        else:
            # Form has errors, display them to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'form_type': 'create'
    })

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    """
    View to edit an existing book. Requires 'can_edit' permission.
    Uses secure form handling and safe database queries.
    """
    try:
        # Safe database query using get_object_or_404
        book = get_object_or_404(Book, id=book_id)
        
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, f'Book "{book.title}" updated successfully!')
                    return redirect('bookshelf:book_list')
                except DatabaseError as e:
                    messages.error(request, 'Database error occurred. Please try again.')
                except Exception as e:
                    messages.error(request, f'Error updating book: {str(e)}')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            form = BookForm(instance=book)
        
        return render(request, 'bookshelf/book_form.html', {
            'form': form,
            'book': book,
            'form_type': 'edit'
        })
        
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
        return redirect('bookshelf:book_list')

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """
    View to delete a book. Requires 'can_delete' permission.
    Uses safe database queries.
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        
        if request.method == 'POST':
            book_title = book.title
            try:
                book.delete()
                messages.success(request, f'Book "{book_title}" deleted successfully!')
                return redirect('bookshelf:book_list')
            except DatabaseError as e:
                messages.error(request, 'Database error occurred. Please try again.')
        
        return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
        
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
        return redirect('bookshelf:book_list')

def home(request):
    """
    Home page view that shows different content based on user permissions.
    Safe from common web vulnerabilities.
    """
    context = {
        'can_view_books': request.user.has_perm('bookshelf.can_view'),
        'can_create_books': request.user.has_perm('bookshelf.can_create'),
        'can_edit_books': request.user.has_perm('bookshelf.can_edit'),
        'can_delete_books': request.user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/home.html', context)