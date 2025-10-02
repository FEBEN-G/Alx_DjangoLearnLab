# Advanced Features Documentation

## Tagging System

### Features
- **Tag Management**: Uses django-taggit for robust tag handling
- **Tag Display**: Tags shown on post lists and detail pages
- **Tag Filtering**: Click any tag to see all posts with that tag
- **Tag Creation**: Add tags when creating/editing posts (comma-separated)

### Usage
1. **Add Tags**: When creating/editing posts, add tags in the tags field
2. **View by Tag**: Click any tag to filter posts
3. **Auto-completion**: django-taggit suggests existing tags

## Search System

### Features
- **Multi-field Search**: Searches title, content, and tags
- **Real-time Results**: Instant search results page
- **Pagination**: Search results are paginated
- **Query Persistence**: Search term persists in results

### Usage
1. **Search**: Use search bar on home page or search results page
2. **Keywords**: Search by post title, content keywords, or tag names
3. **Results**: View matching posts with highlighted relevance

## URLs
- **Search**: `/search/?q=query`
- **Tagged Posts**: `/tags/tag-name/`

## Testing Guidelines

### Tagging Tests
1. Create post with tags "django, python, web"
2. Verify tags display on post list and detail
3. Click a tag → should see filtered posts
4. Edit post → add/remove tags → verify changes

### Search Tests
1. Search for existing post title
2. Search for content keyword
3. Search for tag name
4. Verify empty search shows appropriate message