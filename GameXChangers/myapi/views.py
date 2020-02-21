from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import OwnedGame, Game
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json


# Is get only, developers wont add new games or modify through this but get data of their games
class GameApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        #give people only the data they have access to
        all_games = Game.objects.all().filter(developer=request.user)
        result=[]
        for x in all_games:
        
            times = []
            revenue = 0
            highscores = []
            progresses = []
            for y in OwnedGame.objects.all().filter(game=x):
                dict = {}
                dict['name'] = str(x.name)
                dict['price'] = str(x.price)
                dict['times'] = str(y.bought_at)
                dict['highscore'] = str(y.highscore)
                dict['progress'] = str(y.progress)
                result.append(dict)        
        return Response(result)
