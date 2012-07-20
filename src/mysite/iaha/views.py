from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import Player, GamePre2007, GamePre2010, Game

def index(request):
    return HttpResponse("Hello world.")

def players(request):
    player_list = Player.objects.all()
    return render_to_response('iaha/players.html', {'players': player_list})

def games(request):
    game_list_pre2007 = GamePre2007.objects.all().order_by('id')
    game_list_pre2010 = GamePre2010.objects.all().order_by('id')
    game_list = Game.objects.all().order_by('id')
    return render_to_response('iaha/games.html', {'gamespre2007': game_list_pre2007,
                                                  'gamespre2010': game_list_pre2010,
                                                  'games': game_list})

def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    stats = player.career_stats()
    ps_stats = player.postseason_career_stats()
    return render_to_response('iaha/player.html', {'player': player,
                                                   'stats': stats,
                                                   'ps_stats': ps_stats})
