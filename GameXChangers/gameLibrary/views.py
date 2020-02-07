from django.shortcuts import render
from .models import Game, OwnedGame
from django.contrib.auth.models import User
from .forms import GameForm
from django.http import JsonResponse
import json
from django.http import HttpResponse
# from hashlib import md5
from .paymentHelpers import getChecksum, getPid, getSid, getIncomingChecksum

# Create your views here.

def home(request):
    return render(request, 'gameLibrary/home.html')


# the buygame feature will be implemented here
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

    if request.method == 'GET':
        try:
            owned_game_objects = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
            users_game = OwnedGame.objects.get(player=request.user, game=game_id)
            game = users_game.game
            context = {'game': game, 'owned_game_objects': owned_game_objects, 'users_game': users_game,}
        except Game.DoesNotExist:
            raise Http404("Game does not exist")
    else:
        if 'score' in request.POST:

            try:
                obj = OwnedGame.objects.get(player=request.user, game=game_id)
                if int(request.POST['score']) > obj.highscore: 
                    obj.highscore = int(request.POST['score'])
                    obj.save()
                return JsonResponse({'status': 'Success', 'msg': ' highscore save successfully'})
            except:
                raise Http404("Game not updated")

        elif 'state' in request.POST:

            try:
                obj = OwnedGame.objects.get(player=request.user, game=game_id)
                print(request.POST['state'])
                obj.progress = request.POST['state']
                obj.save()
                return JsonResponse({'status':'Success', 'msg': 'progress save successfully'})
            except:
                raise Http404("GameState not saved")

        elif 'getProgress' in request.POST:

            try:
                obj = OwnedGame.objects.get(player=request.user, game=game_id)
                progress = json.dumps(obj.progress)
                return HttpResponse(progress)

            except:
                raise Http404("Progress not found")

    return render(request, 'gameLibrary/playGame.html', context)


def addGame(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()

            # We also want the user to be able to play the game that she added
            newOwnedGame = OwnedGame(player=request.user, game=game)
            newOwnedGame.save()

    else:
        form = GameForm()

    return render(request, 'gameLibrary/addGame.html', {'form': form})


def developedGames(request):
    my_games = list(filter(lambda x: x.developer == request.user, Game.objects.all()))
    context = {'my_games': my_games}
    return render(request, 'gameLibrary/developedGames.html', context)


# player id found in request.user
def buyGame(request, game_id):
    # user
    # games
    try:
        player = request.user
        game = Game.objects.get(id=game_id)
        pid = getPid(player, game)
        sid = getSid()
        checksum = getChecksum(pid, sid, game.price)
        context = {'game': game, 'pid': pid, 'sid': sid, 'checksum': checksum, 'player': player}
        return render(request, 'gameLibrary/buyGame.html', context)
    except:
        raise Http404("Game not found")


def success(request):

    # get returns None if not found.
    checksum = getIncomingChecksum(request.GET.get("pid"), request.GET.get("ref"), request.GET.get("result"))
    isValid = checksum == request.GET.get("checksum")
    if isValid:
        # first get the pid from the request
        pid = request.GET.get("pid")
        # then get player and game ids from the pid
        divider1 = pid.find(':')
        divider2 = pid.find('/')
        player_id = pid[0:divider1]
        game_id = pid[divider1+1:divider2]
        # then get the player and game corresponding to them
        player = User.objects.get(id=player_id)
        game = Game.objects.get(id=game_id)
        # then make a new ownedgame and save it
        newOwnedGame = OwnedGame(player=player, game=game)
        newOwnedGame.save()
        context = {'game': game}
        return render(request, 'gameLibrary/success.html', context)
    else:
        return render(request, 'gameLibrary/error.html')


def error(request):
    return render(request, 'gameLibrary/error.html')
