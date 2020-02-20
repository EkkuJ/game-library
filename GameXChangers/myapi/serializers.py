from rest_framework import serializers

from .models import OwnedGame, Game

class OwnedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OwnedGame
        fields = ('progress', 'bought_at')
        
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'description', 'url', 'highscore','price','players','developer', 'price')
