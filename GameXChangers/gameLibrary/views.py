from django.shortcuts import render
from .models import Game, OwnedGame
from django.contrib.auth.models import User
from .forms import GameForm
from django.http import JsonResponse
import json

# Create your views here.

def home(request):
    return render(request, 'gameLibrary/home.html')

def browseGames(request):

    game_list = Game.objects.all()
    owned_game_objects = list(filter(lambda x: x.player == request.user, OwnedGame.objects.all()))
    owned_game_list = list(map(lambda x: x.game, owned_game_objects))
    context = {'game_list': game_list, 'owned_game_list': owned_game_list}
    return render(request, 'gameLibrary/browseGames.html', context)

def myGames(request):
    my_games = list(filter(lambda x: x.player == request.user, OwnedGame.objects.all()))
    context = {'my_games': my_games}
    return render(request, 'gameLibrary/myGames.html', context)

# Show gaming view for specific game
def playGame(request, game_id):
    print(game_id)
    if request.method == 'GET':
        try:
            game = Game.objects.get(pk=game_id)
            owned_game_objects = list(filter(lambda x: x.game.id == game_id,
            OwnedGame.objects.all()))
            users_game = OwnedGame.objects.get(player = request.user, game = game_id)
            context = {'game': game, 'owned_game_objects': owned_game_objects, 'users_game': users_game,}
        except Game.DoesNotExist:
            raise Http404("Game does not exist")
    else:
        if 'score' in request.POST:

            try:
                obj = OwnedGame.objects.get(player=request.user, game = game_id)
                if int(request.POST['score']) > obj.highscore: 
                    obj.highscore = int(request.POST['score'])
                    obj.save()
                return JsonResponse({'status':'Success', 'msg': ' highscore save successfully'})
            except:
                raise Http404("Game not updated")

        elif 'state' in request.POST:

            try:
                obj = OwnedGame.objects.get(player=request.user, game = game_id)
                obj.progress = json.loads(request.POST['state'])
                obj.save()  
                return JsonResponse({'status':'Success', 'msg': 'progress save successfully'})
            except:
                raise Http404("GameState not saved")

    return render(request, 'gameLibrary/playGame.html', context)


def addGame(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()
    
    else:
        form = GameForm()

    return render(request, 'gameLibrary/addGame.html', {'form': form})
