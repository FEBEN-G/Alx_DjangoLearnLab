from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book
from .forms import BookForm

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Retrieve the book or return 404 if not found
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        # Bind form to POST data and file data if any
        form = BookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('book_list')  # Redirect to a book list page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # If GET request, prefill the form with existing book data
        form = BookForm(instance=book)

    context = {
        "form": form,
        "book": book
    }
    return render(request, 'bookshelf/edit_book.html', context)
def book_list(request):
    query = request.GET.get('search', '')  # Get search term from query params
    if query:
        books = Book.objects.filter(title__icontains=query)  # ORM safe query
    else:
        books = Book.objects.all()

    return render(request, "bookshelf/book_list.html", {"books": books, "search": query})
