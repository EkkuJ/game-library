from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django import forms

SIGN_IN_CHOICES = [
('developer', 'Developer'),
('player', 'Player'),
]

class MyUserCreationForm(auth_forms.UserCreationForm):
    sign_up_as = forms.ChoiceField(choices=SIGN_IN_CHOICES, label='Sign up as:')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]

