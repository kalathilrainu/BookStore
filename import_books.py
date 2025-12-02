import os
import pandas as pd
from bookadmin.models import Book, Category
from django.contrib.auth.models import User

# === Path to your Excel ===
excel_path = r"D:\Python\BookStore\malayalam_books.xlsx"  # or use your new file

# Load Excel data
df = pd.read_excel(excel_path)

# Assign books to superuser (optional)
admin_user = User.objects.filter(is_superuser=True).first()

added, skipped = 0, 0

for index, row in df.iterrows():
    title = str(row['Title']).strip()
    author = str(row['Author']).strip()
    category_name = str(row['Category']).strip()
    price = float(row['Price_Rs'])
    cover_file = str(row['Cover_Image']).strip() if 'Cover_Image' in row else None

    # Get or create category
    category, created = Category.objects.get_or_create(name=category_name)

    # Avoid duplicate books (case-insensitive match)
    if Book.objects.filter(title__iexact=title, author__iexact=author).exists():
        skipped += 1
        continue

    # Create the new Book
    book = Book.objects.create(
        title=title,
        author=author,
        category=category,
        price=price,
        cover=cover_file,
        created_by=admin_user
    )

    added += 1
    print(f"✅ Added: {book.title} ({category.name})")

print(f"\n🎉 Import completed: {added} new books added, {skipped} skipped (already existed).")
