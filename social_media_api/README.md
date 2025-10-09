# Social Media API

A Django REST Framework-based Social Media API with user authentication, posts, comments, follows, likes, and notifications.

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
## Features

- JWT Authentication
- User registration and login
- User profiles with bio and profile pictures
- Follow/Unfollow system
- Posts and comments
- Likes system
- Notifications
- Feed functionality

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - User profile
- `GET /api/auth/users/` - List all users

### Posts & Comments
- `GET /api/posts/posts/` - List all posts
- `POST /api/posts/posts/` - Create a post
- `GET /api/posts/posts/{id}/` - Get post details
- `POST /api/posts/posts/{id}/like/` - Like a post
- `POST /api/posts/posts/{id}/unlike/` - Unlike a post
- `GET /api/posts/feed/` - Personalized feed

### Notifications
- `GET /api/notifications/notifications/` - List user notifications
- `GET /api/notifications/notifications/unread/` - Unread notifications
- `POST /api/notifications/notifications/mark_all_as_read/` - Mark all as read
- `POST /api/notifications/notifications/{id}/mark_as_read/` - Mark as read
- `POST /api/notifications/notifications/{id}/mark_as_unread/` - Mark as unread
- `GET /api/notifications/notifications/count/` - Notification counts

## Testing Notifications

### Get Notification Count
```bash
GET /api/notifications/notifications/count/
Authorization: Bearer <token>
## Testing with Postman

### User Registration
```json
POST /api/auth/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "bio": "Test bio"
}