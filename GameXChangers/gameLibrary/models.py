
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


# Model User comes directly from django.contri.auth.
# https://docs.djangoproject.com/en/3.0/ref/contrib/auth/


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(default='Game Description')
    url = models.URLField(blank=True)
    highscore = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    # May be more efficient to store the "player-game" -relation
    # in the User-model. To be considered
    players = models.ManyToManyField(User, related_name='games',through='OwnedGame')
    developer = models.ForeignKey(User, related_name='game_developed', on_delete=models.CASCADE, default=1)

    def str(self):
        return self.name


class OwnedGame(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    bought_at = models.DateTimeField(default=timezone.now)
    # 0-100
    progress = models.TextField(blank=True) # json object converted to string
    highscore = models.IntegerField(default=0)

    def str(self):
        return self.name

