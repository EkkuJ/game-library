from django.shortcuts import render, redirect
from .models import Game, OwnedGame
from django.contrib.auth.models import User
from .forms import GameForm, ModifyForm
from django.http import JsonResponse
import json
from django.http import HttpResponse
# from hashlib import md5
from .paymentHelpers import getChecksum, getPid, getSid, getIncomingChecksum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from itertools import chain


# Create your views here.


def home(request):
    return render(request, 'gameLibrary/home.html')


# the buygame feature will be implemented here
def browseGames(request):
    #get the possible search data from the request
    search = request.GET.get('search')
    game_list = Game.objects.all()
    # change the gamelist to match the search results
    if search:
        nameResult = Game.objects.filter(name__contains=search)
        descResult = Game.objects.filter(description__contains=search)
        game_list = list(chain(nameResult, descResult))
    
    owned_game_objects = list(filter(lambda x: x.player == request.user, OwnedGame.objects.all()))
    owned_game_list = list(map(lambda x: x.game, owned_game_objects))
    context = {'game_list': game_list, 'owned_game_list': owned_game_list}
    return render(request, 'gameLibrary/browseGames.html', context)

@login_required
def myGames(request):
    my_games = list(filter(lambda x: x.player == request.user, OwnedGame.objects.all()))
    context = {'my_games': my_games}
    return render(request, 'gameLibrary/myGames.html', context)

# Show gaming view for specific game
@login_required
def playGame(request, game_id):

    if request.method == 'GET':
        try:
            owned_game_objects = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
            users_game = OwnedGame.objects.get(player=request.user, game=game_id)
            game = users_game.game
            context = {'game': game, 'owned_game_objects': owned_game_objects, 'users_game': users_game,}
        except Game.DoesNotExist:
            raise Http404("Game does not exist")
    elif request.method == 'POST':
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

    else:
        return Http404("Request not found")

    return render(request, 'gameLibrary/playGame.html', context)

def preview(request, game_id):

    game = Game.objects.get(id=game_id)
    owned_game_objects = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
    context = {'game': game, 'ownedGames': owned_game_objects}

    return render(request, 'gameLibrary/preview.html', context)

def is_developer(user):
    boolvalue = user.groups.filter(name='Developer').exists()
    # print(boolvalue)
    return boolvalue


@login_required
@user_passes_test(is_developer, login_url='/gameLibrary')
def addGame(request):

    try:
        # if user posts through the form
        if request.method == 'POST':
            form = GameForm(request.POST)
            context = {'form':form}
            if form.is_valid():
                game = form.save(commit=False)
                game.developer = request.user
                game.save()

                # We also want the user to be able to play the game that she added
                newOwnedGame = OwnedGame(player=request.user, game=game)
                newOwnedGame.save()
                # If succesful until here, redirect user to their own game folder 
                # with success message
                messages.success(request, 'Successfully added the game')
                return redirect('/developedGames')
        # in case of get request, that means when user comes to page first time
        elif request.method == 'GET':
            form = GameForm()
            context = {'form':form}
            return render(request, 'gameLibrary/addGame.html', context)
        else:
            raise Exception('')
    except Exception:
        messages.warning(request, "Adding the game didn't go through")
        context = {}
        return render(request, 'gameLibrary/addGame.html', context)

def api(request):

    all_games = (Game.objects.all())
    mapped = json.dumps(list(map(lambda g: g.name, all_games)))

    return render(request, 'gameLibrary/api.html', {'mapped': mapped})


@login_required
@user_passes_test(is_developer, login_url='/gameLibrary')
def developedGames(request):
    my_games = list(filter(lambda x: x.developer == request.user, Game.objects.all()))
    context = {'my_games': my_games}
    return render(request, 'gameLibrary/developedGames.html', context)


@login_required
@user_passes_test(is_developer, login_url='/gameLibrary')
def removeGame(request, game_id):
    try:
        # We get the game from ownedgames with the users id and given game_id.
        # this must be done to all the ownedgame objects
        # owned_games = OwnedGame.objects.get(player=request.user, game=game_id)
        owned_game_objects = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
        # If there is no such ownedGame, the next line will throw a Game.DoesNotExist. Shouldn't happen though
        game = owned_game_objects[0].game
        # If the user is the developer, they can delete the game
        if game.developer == request.user:
            game.delete()
            # we delete the ownedGame object from all users
            for x in owned_game_objects:
                x.delete()
            owned_game_objects_after = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
            messages.success(request, 'Successful removal of the game')
        else:
            raise Exception('')
    except Exception:
        messages.warning(request, 'Failed to remove the game')

    # Get the data to pass to the developedGames template
    my_games = list(filter(lambda x: x.developer == request.user, Game.objects.all()))
    context = {'my_games': my_games}

    return render(request, 'gameLibrary/developedGames.html', context)

# also must be the developer of the game.
@login_required
@user_passes_test(is_developer, login_url='/gameLibrary')
def modifyGame(request, game_id):
    try:
    
        # First we get the game to check if user is the developer of that game
        gameFetched = Game.objects.get(id=game_id)
        # print(request.method == 'POST')
        if gameFetched.developer == request.user:
            form = ModifyForm(request.POST)
            game = form.save(commit=False)
            # The next lines will not be affected by the form
            game.developer = request.user
            game.id = game_id
            game.name = gameFetched.name
            context = {'form':form, 'name':game.name}
            # if user is posting
            if form.is_valid() and request.method == 'POST':
                
                # If the form has blank spaces,we dont want to change the game
                if game.url == '':
                    game.url = gameFetched.url
                if game.price == None:
                    game.price = gameFetched.price
                if game.description == '':
                    game.description = gameFetched.description
                game.save()
                messages.success(request, 'Successfully modified the game')
                return redirect('/developedGames')
            # if user just came to the site
            elif request.method == 'GET':
                return render(request, 'gameLibrary/modifyGame.html', context)
            # failure
            else:
                raise Exception('')
    except Exception:
        # messages.warning(request, 'Failed to modify the game' )
        context = {}
        messages.warning(request, 'Failed to modify the game' )
        return render(request, 'gameLibrary/modifyGame.html', context)

@login_required
@user_passes_test(is_developer, login_url='/gameLibrary')
def gameStats(request, game_id):
    try:
        # First get the game
        game= Game.objects.get(id=game_id)
        listOfGames = list(filter(lambda x: x.game.id == game_id, OwnedGame.objects.all()))
        # The amount how many people have bought this game:
        amount = len(listOfGames)
        # The list of all timestamp-player pairs
        timestampList = []
        for x in listOfGames:
            timestampList.append( str(x.bought_at.date()) +' : ' + str(x.player))
        context = {'amount':amount, 'timestampList':timestampList } 
    except Exception:
        context={}
        messages.warning(request,"The game stats search didn't go through.")
    return render(request, 'gameLibrary/gameStats.html', context)


class HasAlready(Exception):
    pass

# player id found in request.user
@login_required
def buyGame(request, game_id):
    context = {}
    try:
        # Only let the user buy games if they dont have it already
        game = Game.objects.get(id=game_id)
        player = request.user
        #check how many ownedgame objects there are for player and game match
        hasGame = OwnedGame.objects.all().filter(player=player, game=game_id)
        # if zero...
        if len(hasGame)==0:
            pid = getPid(player, game)
            sid = getSid()
            checksum = getChecksum(pid, sid, game.price)
            context = {'game': game, 'pid': pid, 'sid': sid, 'checksum': checksum, 'player': player, 'hasGame':False}
            return render(request, 'gameLibrary/buyGame.html', context)
        # if more than zero
        else:
            raise HasAlready
    except HasAlready:
        messages.warning(request, 'You already have the game you tried to purchase')
        context = {'hasGame':True}
        return render(request, 'gameLibrary/buyGame.html', context)
    except Exception as e:
        messages.warning(request, 'Failed to buy the game')
    return render(request, 'gameLibrary/buyGame.html', context)

@login_required
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

        # This could also be implemented by giving a error message and rendering
        # the browseGames/playGame
        return render(request, 'gameLibrary/success.html', context)
    else:
        return render(request, 'gameLibrary/error.html')


@login_required
def error(request):
    return render(request, 'gameLibrary/error.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
