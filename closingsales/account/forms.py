from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User

class SignUpForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Name des Geschäfts',
            'autocomplete': 'off'
        }
    ))
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Geschäftliche E-Mail',
            'autocomplete': 'off'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Passwort',
            'autocomplete': 'off'
            }
        ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Passwort Wiederholen'
        }
    ))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Geschäftstelefonnummer'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'password1',  'password2')
