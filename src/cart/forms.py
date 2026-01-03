import re
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Imię',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Imię*',
        })
    )

    last_name = forms.CharField(
        label='Nazwisko',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nazwisko*',
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email*',
        })
    )

    phone = forms.CharField(
        label='Nr telefonu',
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nr telefonu*',
            'pattern': r'\d{9}',
        }),
        help_text="<span class='form-text text-muted small'>Wpisz 9-cyfrowy numer, bez +48 i bez spacji</span>"
    )

    street_address = forms.CharField(
        label='Ulica i numer',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ulica i numer*',
        })
    )

    postal_code = forms.CharField(
        label='Kod pocztowy',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kod pocztowy*',
            'pattern': r'\d{2}-\d{3}',
        }),
        help_text="<span class='form-text text-muted small'>Format XX-XXX</span>"
    )

    city = forms.CharField(
        label='Miasto',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Miasto*',
        })
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'street_address', 'postal_code', 'city']

    def clean_postal_code(self):
        code = self.cleaned_data['postal_code']
        if not re.match(r'^\d{2}-\d{3}$', code):
            raise forms.ValidationError("Kod pocztowy musi być w formacie XX-XXX.")
        return code

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{9}$', phone):
            raise forms.ValidationError("Numer telefonu musi zawierać 9 cyfr.")
        return phone
