from django.urls import path
from . import views

urlpatterns = [
    path('add-book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('categories/', views.category_list, name='category_list'),
    path('add-category/', views.add_category, name='add_category'),
    path('category/<int:category_id>/books/', views.books_by_category, name='books_by_category'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('books/<int:id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:id>/delete/', views.delete_book, name='delete_book'),
    path('users/', views.user_list, name='user_list'),

]
