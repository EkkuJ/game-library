from rest_framework import serializers

from .models import OwnedGame, Game

class OwnedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OwnedGame
        fields = ('progress', 'bought_at')