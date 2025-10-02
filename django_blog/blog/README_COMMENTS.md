# Comment System Documentation

## Features Implemented

### 1. Comment Model
- **Fields**: post (ForeignKey), author (ForeignKey), content (TextField), created_at, updated_at
- **Relations**: Many-to-one with Post, Many-to-one with User
- **Ordering**: Newest comments first

### 2. Comment Operations
- **Add Comment**: Authenticated users can comment on any post
- **Edit Comment**: Authors can edit their own comments
- **Delete Comment**: Authors can delete their own comments
- **View Comments**: All users can read comments

### 3. URLs
- **Add Comment**: `/post/<post_id>/comment/` (POST)
- **Edit Comment**: `/comment/<comment_id>/edit/`
- **Delete Comment**: `/comment/<comment_id>/delete/`

### 4. Permissions
- **Read**: Public (no authentication required)
- **Create**: Authenticated users only
- **Update/Delete**: Comment author only

## Testing Guidelines

1. **Add Comment**: 
   - Login → Go to post → Fill comment form → Submit
   - Should see success message and comment appear

2. **Edit Comment**:
   - Login → Your comment → Edit → Modify → Submit
   - Should see updated comment and timestamp

3. **Delete Comment**:
   - Login → Your comment → Delete → Confirm
   - Should see success message and comment removed

4. **Security Test**:
   - Try editing/deleting other users' comments (should be blocked)
   - Try commenting without login (should see login prompt)