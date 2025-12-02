from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


# 🧩 REGISTER VIEW
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation
        if not username or not password:
            return render(request, 'register.html', {'error': 'Please provide both username and password.'})

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken!'})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')


# 🧩 LOGIN VIEW
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'error': 'Your account is inactive. Contact admin.'})

            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')

            # Redirect admins to admin dashboard, users to normal dashboard
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            else:
                # Support "next" parameter for redirects
                next_url = request.GET.get('next') or 'dashboard'
                return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')


# 🧩 LOGOUT VIEW
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


# 🧩 USER DASHBOARD (Normal Users)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    """
    Redirect user directly to book list after login.
    """
    return redirect('book_list')  # Redirect to Book List page



# 🧩 ADMIN CHECK HELPER
def is_admin(user):
    return user.is_superuser or user.is_staff


# 🧩 ADMIN DASHBOARD (Only for Admins)
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    """
    Dedicated Admin Dashboard
    """
    from bookadmin.models import Book, Category
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()

    return render(request, 'admin_dashboard.html', {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_users': total_users,
    })
