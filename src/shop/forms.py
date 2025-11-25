from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz email',
        }),
        error_messages={
            'required': 'Email nie może być pusty.'
        },
    )
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz hasło',
        }),
        error_messages={
            'required': 'Hasło nie może być puste.',
        },
    )

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Imię',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz imię',
        }),
    )
    last_name = forms.CharField(
        label='Nazwisko',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz nazwisko',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Wpisz email'
        self.fields['email'].label = 'Email'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Wpisz hasło'
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Hasło nie może składać się wyłącznie z cyfr.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Potwierdź hasło'
        self.fields['password2'].label = 'Potwierdź hasło'
        self.fields['password2'].help_text = ''