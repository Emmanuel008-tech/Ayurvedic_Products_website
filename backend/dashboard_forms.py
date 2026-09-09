from django import forms
from .models import Product, Enquiry


class DashboardLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter staff username (e.g. admin)',
            'class': 'form-input',
            'autocomplete': 'username',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-input',
            'autocomplete': 'current-password',
            'id': 'id_password'
        })
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock_quantity', 'description', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. KeshVeda Herbal Hair Oil',
                'class': 'form-input',
                'id': 'id_name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_category'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '499.00',
                'step': '0.01',
                'class': 'form-input',
                'id': 'id_price'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'placeholder': '25',
                'min': '0',
                'class': 'form-input',
                'id': 'id_stock_quantity'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Detailed herbal description, classical preparation, botanical ingredients...',
                'class': 'form-textarea',
                'rows': 4,
                'id': 'id_description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'id': 'id_image',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
                'id': 'id_is_active'
            }),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive amount in INR.")
        return price
