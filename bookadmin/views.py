from django.db.models import Q
from .models import Book, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookModelForm
from .models import Book
from django.contrib.auth.decorators import user_passes_test


# ✅ Step 3: Add Book using ModelForm
@login_required
def add_book(request):
    """
    Add a new book entry using the BookModelForm.
    Links the book to the logged-in user and saves uploaded cover images.
    """
    if request.method == 'POST':
        form = BookModelForm(request.POST, request.FILES)  # handle file uploads too
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookModelForm()

    return render(request, 'add_book.html', {'form': form})


# ✅ Step 4: Book List (Dashboard)
@login_required

def book_list(request):
    """
    Displays all books, with optional filters by category and author.
    """
    category_filter = request.GET.get('category', '')
    author_filter = request.GET.get('author', '')

    books = Book.objects.all().order_by('-id')

    # Filter logic
    if category_filter:
        books = books.filter(category__name__icontains=category_filter)
    if author_filter:
        books = books.filter(author__icontains=author_filter)

    categories = Category.objects.all().order_by('name')  # for dropdown options

    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_filter,
        'author_filter': author_filter,
    }
    return render(request, 'book_list.html', context)



# Optional dashboard placeholder view (can be removed or expanded later)
def dashboard(request):
    return render(request, 'dashboard.html')


# ✅ Step 5: Book Detail
@login_required
def book_detail(request, pk):
    """
    Display a single book's full details.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})


# ✅ Step 5: Edit / Update Book
@login_required
def edit_book(request, pk):
    """
    Edit an existing book record.
    """
    book = get_object_or_404(Book, pk=pk)

    # Only allow editing if the logged-in user created the book or is admin
    if book.created_by != request.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this book.")
        return redirect('book_list')

    if request.method == 'POST':
        form = BookModelForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookModelForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})


# ✅ Step 5: Delete Book
@login_required
def delete_book(request, pk):
    """
    Delete a book entry.
    """
    book = get_object_or_404(Book, pk=pk)

    # Only allow deleting if created by same user or admin
    if book.created_by != request.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this book.")
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')

    return render(request, 'delete_book.html', {'book': book})


from .models import Book, Category
from .forms import BookModelForm, CategoryForm


@login_required
def category_list(request):
    cat = Category.objects.all().order_by('name')
    return render(request, 'category_list.html', {'cat': cat})


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


@login_required
def books_by_category(request, category_id):
    """
    Display all books that belong to a given category.
    """
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all().order_by('-created_at')  # thanks to related_name='books'
    return render(request, 'books_by_category.html', {'category': category, 'books': books})


from django.contrib.auth.models import User

@login_required
def admin_dashboard(request):
    """
    Stylish admin dashboard with counts and quick links.
    """
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()

    return render(request, 'admin_dashboard.html', {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_users': total_users,
    })


# Only staff or superuser can edit books
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def edit_book(request, id):
    """
    Allows admin/staff to edit a book using the BookModelForm.
    """
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookModelForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookModelForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})


from django.shortcuts import render, get_object_or_404, redirect

@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    # Show confirmation page before deletion
    return render(request, 'delete_book.html', {'book': book})


# bookadmin/views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# ... your existing imports and views ...


@login_required
def user_list(request):
    """Show all registered users to the admin."""
    users = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'users': users})
