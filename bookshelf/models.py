from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation with email instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the primary identifier
    instead of username, with additional fields.
    """
    # Remove the username field and use email instead
    username = None
    email = models.EmailField('email address', unique=True)
    date_of_birth = models.DateField('date of birth', null=True, blank=True)
    profile_photo = models.ImageField(
        'profile photo', 
        upload_to='profile_photos/', 
        null=True, 
        blank=True
    )
    
    # Set email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'email' from REQUIRED_FIELDS

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

class Book(models.Model):
    """
    Book model with custom permissions for access control.
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    author = models.CharField(max_length=100, help_text="Author of the book")
    isbn = models.CharField(
        max_length=13, 
        unique=True, 
        help_text="International Standard Book Number"
    )
    publication_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Date when the book was published"
    )
    description = models.TextField(
        blank=True, 
        help_text="Brief description of the book"
    )
    created_by = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE,
        related_name='books_created',
        help_text="User who created this book record"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} by {self.author}"