import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()

# Now import your model
from imdb.models import TitleBasics

# Create and save some instances
book1 = TitleBasics(
    tconst = "a",
    title_type = "b",
    primary_title = "c",
    original_title = "d",
    is_adult = True,
    start_year = "2024",
    end_year = "2025",
    runtime_minutes = "106",
    genres = "e"
)
book1.save()

book2 = TitleBasics(
    tconst = "b",
    title_type = "c",
    primary_title = "d",
    original_title = "e",
    is_adult = True,
    start_year = "2024",
    end_year = "2025",
    runtime_minutes = "106",
    genres = "f"
)
book2.save()

print("Books added successfully!")


TitleBasics.objects.bulk_create([
    TitleBasics(
    tconst = "c",
    title_type = "c",
    primary_title = "d",
    original_title = "e",
    is_adult = True,
    start_year = "2024",
    end_year = "2025",
    runtime_minutes = "106",
    genres = "f"
),
TitleBasics(
    tconst = "d",
    title_type = "c",
    primary_title = "d",
    original_title = "e",
    is_adult = True,
    start_year = "2024",
    end_year = "2025",
    runtime_minutes = "106",
    genres = "f"
)
])

print("bulk import completed.")


"""
from myapp.models import Book
from datetime import date
import random

books = []

for i in range(500):
    book = Book(
        title=f"Book {i + 1}",
        author=f"Author {random.randint(1, 100)}",
        published_date=date(2000 + i % 20, random.randint(1, 12), random.randint(1, 28))
    )
    books.append(book)

# Insert all at once
Book.objects.bulk_create(books)

print("500 books inserted!")
"""