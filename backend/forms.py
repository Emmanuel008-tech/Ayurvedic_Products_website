from django import forms
from django.core.validators import RegexValidator
from .models import Product, Enquiry


class EnquiryForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 9876543210',
            'class': 'form-input',
            'id': 'id_phone_number',
            'autocomplete': 'tel',
        }),
        validators=[
            RegexValidator(
                regex=r'^(?:\+?91)?[6-9]\d{9}$',
                message='Please enter a valid 10-digit Indian phone number (e.g. 9876543210).'
            )
        ],
        error_messages={
            'required': 'Phone number is required so we can respond to your enquiry.',
        }
    )

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Full Name',
            'class': 'form-input',
            'id': 'id_name',
            'autocomplete': 'name',
        }),
        error_messages={
            'required': 'Please provide your name.',
        }
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),  # Dynamically populated in __init__
        empty_label="-- Select an Ayurvedic Product --",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_product',
        }),
        error_messages={
            'required': 'Please select a product you are interested in.',
        }
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your requirement or ask any questions about our ingredients...',
            'class': 'form-textarea',
            'rows': 4,
            'id': 'id_message',
        }),
        required=False
    )

    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'product', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True).order_by('name')

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
