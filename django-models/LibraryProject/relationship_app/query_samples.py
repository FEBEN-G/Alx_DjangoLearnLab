# relationship_app/query_samples.py
def run_queries():
    from .models import Author, Book, Library, Librarian
    # NOTE: run this by importing run_queries inside manage.py shell:
    # python manage.py shell
    # >>> from relationship_app.query_samples import run_queries
    # >>> run_queries()

    # Query all books by a specific author name
    author_name = "George Orwell"
    author_qs = Author.objects.filter(name=author_name)
    if author_qs.exists():
        a = author_qs.first()
        print(f"Books by {a.name}:")
        for b in Book.objects.filter(author=a):
            print(f" - {b.title} ({b.publication_year})")
    else:
        print("No author named:", author_name)

    # List all books in a library
    library_name = "Central Library"
    lib_qs = Library.objects.filter(name=library_name)
    if lib_qs.exists():
        lib = lib_qs.first()
        print(f"Books in {lib.name}:")
        for b in lib.books.all():
            print(f" - {b.title}")
    else:
        print("No library named:", library_name)

    # Retrieve the librarian for a library (if exists)
    if lib_qs.exists():
        lib = lib_qs.first()
        try:
            libn = Librarian.objects.get(library=lib)
            print(f"Librarian for {lib.name} is {libn.name}")
        except Librarian.DoesNotExist:
            print("No librarian for library", lib.name)

