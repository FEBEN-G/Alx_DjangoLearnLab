from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books with proper validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 13-digit ISBN'
            }),
            'publication_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter book description (optional)'
            }),
        }
    
    def clean_title(self):
        """Sanitize and validate title field."""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError('Title is required.')
        
        # Basic XSS protection - remove script tags
        title = title.replace('<script>', '').replace('</script>', '')
        
        if len(title) > 200:
            raise ValidationError('Title must be less than 200 characters.')
        
        return title
    
    def clean_author(self):
        """Sanitize and validate author field."""
        author = self.cleaned_data.get('author', '').strip()
        if not author:
            raise ValidationError('Author is required.')
        
        # Basic XSS protection
        author = author.replace('<script>', '').replace('</script>', '')
        
        if len(author) > 100:
            raise ValidationError('Author name must be less than 100 characters.')
        
        return author
    
    def clean_isbn(self):
        """Validate ISBN format."""
        isbn = self.cleaned_data.get('isbn', '').strip()
        if not isbn:
            raise ValidationError('ISBN is required.')
        
        # Remove any hyphens or spaces
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # Validate ISBN length (10 or 13 digits)
        if len(isbn) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 digits long.')
        
        # Validate that ISBN contains only digits
        if not isbn.isdigit():
            raise ValidationError('ISBN must contain only numbers.')
        
        return isbn
    
    def clean_description(self):
        """Sanitize description field."""
        description = self.cleaned_data.get('description', '').strip()
        
        # Basic XSS protection
        if description:
            description = description.replace('<script>', '').replace('</script>', '')
        
        return description