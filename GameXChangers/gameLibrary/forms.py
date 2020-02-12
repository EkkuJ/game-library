from django import forms
from gameLibrary.models import Game, OwnedGame

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'description', 'url', 'price',)

class ModifyForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ( 'description', 'url', 'price',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['url'].required = False
        self.fields['price'].required = False

