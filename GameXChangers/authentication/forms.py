from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django import forms

SIGN_IN_CHOICES = [
('developer', 'Developer'),
('player', 'Player'),
]

class MyUserCreationForm(auth_forms.UserCreationForm):
    sign_up_as = forms.ChoiceField(choices=SIGN_IN_CHOICES, label='Sign up as:')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'sign_up_as']

