from django import forms
from .models import Book, Category 


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'price', 'description', 'cover']
        labels = {
            'category': 'Select Category',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    # ✅ Custom validation examples
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError("Title must have at least 2 characters.")
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Category Name',
            'description': 'Description (optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
