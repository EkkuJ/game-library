from django import forms
from gameLibrary.models import Game, OwnedGame

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'description', 'url', 'price',)
