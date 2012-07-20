from django.db.models import Q

def win_pct(games, wins):
    try:
        pct = '%.3f' % round(float(wins) / games, 3)
        if pct[0] == '0':
            pct = pct[1:]
        return pct
    except:
        return '.000'

def g_rate(games, goals):
    try:
        return '%.2f' % round(float(goals) / games, 2)
    except:
        return '0.00'


class GameStats:
    player = None
    game = None
    opponent = None
    outcome = 'L'
    gf = ga = og = ogo = a = ao = 0
    gs = go = 0
    
    def __init__(self, player, game):
        from models import GamePre2007, GamePre2010, Game
        if not game.player1 == player and not game.player2 == player:
            raise Exception(str(player) + ' is not in ' + str(game))
        self.player = player
        self.game = game
        if type(game) is GamePre2007:
            self.og = self.ogo = self.a = self.ao = self.gs = self.go = ' '
            if game.player1 == player:
                self.opponent = game.player2
                self.gf = game.p1_gf
                self.ga = game.p2_gf
                if game.winner() == 'p1':
                    self.outcome = 'W'
            else:
                self.opponent = game.player1
                self.gf = game.p2_gf
                self.ga = game.p1_gf
                if game.winner() == 'p2':
                    self.outcome = 'W'
        elif type(game) is GamePre2010:
            if game.player1 == player:
                self.opponent = game.player2
                self.gf = game.p1_gf
                self.ga = game.p2_gf
                self.og = game.p1_og
                self.ogo = game.p2_og
                self.a = game.p1_a
                self.ao = game.p2_a
                if game.winner() == 'p1':
                    self.outcome = 'W'
            else:
                self.opponent = game.player1
                self.gf = game.p2_gf
                self.ga = game.p1_gf
                self.og = game.p2_og
                self.ogo = game.p1_og
                self.a = game.p2_a
                self.ao = game.p1_a
                if game.winner() == 'p2':
                    self.outcome = 'W'
            self.gs = self.gf - self.ogo
            self.go = self.ga - self.og
        elif type(game) is Game:
            pass # TODO: Crunch numbers for games 2010+

        
class WeekStats:
    game_stats = None
    player = None
    week = None
    w = l = gf = ga = og = ogo = a = ao = 0
    g = wpct = gs = go = gfg = gsg = gag = gog = ogg = 0
    
    def __init__(self, player, week):
        from models import WeekPre2007, GamePre2007, GamePre2010
        self.game_stats = []
        self.player = player
        self.week = week
        if week.season.year < 2007:
            self.gs = self.ogo = self.gsg = self.ao = ' '
            try:
                w = WeekPre2007.objects.get(week=week, player=player)
                self.og = w.og
                self.a = w.a
            except:
                pass
            for game in GamePre2007.objects.filter(Q(player1=player) |
                                                   Q(player2=player),
                                                   week=week).order_by('id'):
                g = GameStats(player, game)
                self.game_stats.append(g)
                self.gf += g.gf
                self.ga += g.ga
                if g.outcome == 'W':
                    self.w += 1
                else:
                    self.l += 1
            
        elif week.season.year < 2010:
            for game in GamePre2010.objects.filter(Q(player1=player) |
                                                   Q(player2=player),
                                                   week=week).order_by('id'):
                g = GameStats(player, game)
                self.game_stats.append(g)
                self.gf += g.gf
                self.ga += g.ga
                self.og += g.og
                self.ogo += g.ogo
                self.a += g.a
                self.ao += g.ao
                if g.outcome == 'W':
                    self.w += 1
                else:
                    self.l += 1
            self.g = self.w + self.l
            self.gs = self.gf - self.ogo
            self.gsg = g_rate(self.g, self.gs)
        else:
            pass # TODO: Crunch numbers for weeks 2010+
        self.g = self.w + self.l
        self.wpct = win_pct(self.g, self.w)
        self.go = self.ga - self.og
        self.gfg = g_rate(self.g, self.gf)
        self.gag = g_rate(self.g, self.ga)
        self.gog = g_rate(self.g, self.go)
        self.ogg = g_rate(self.g, self.og)
         

class SeasonStats:
    week_stats = None
    player = None
    season = None
    age = 0
    league = ''
    w = l = gf = ga = og = ogo = a = ao = 0
    g = wpct = gs = go = gfg = gsg = gag = gog = ogg = 0
    
    def __init__(self, player, season):
        from models import Week, PlayerLeagueBySeason
        self.week_stats = []
        self.player = player
        self.season = season
        self.age = player.age(season)
        self.league = PlayerLeagueBySeason.objects.get(player=player,
                                                       season=season
                                                       ).get_league_display
        for week in Week.objects.filter(season=season).order_by('week_num'):
            w = WeekStats(player, week)
            if len(w.game_stats) > 0:
                self.week_stats.append(w)
                self.w += w.w
                self.l += w.l
                self.gf += w.gf
                self.ga += w.ga
                self.og += w.og
                self.a += w.a
                if season.year < 2007:
                    self.ogo = self.ao = self.gs = self.gsg = ' '
                else:
                    self.ogo += w.ogo
                    self.ao += w.ao
                    self.gs += w.gs
                    self.gsg = g_rate(self.w + self.l, self.gs)
        self.g = self.w + self.l
        self.wpct = win_pct(self.g, self.w)
        self.go = self.ga - self.og
        self.gfg = g_rate(self.g, self.gf)
        self.gag = g_rate(self.g, self.ga)
        self.gog = g_rate(self.g, self.go)
        self.ogg = g_rate(self.g, self.og)


class CareerStats:
    season_stats = None
    player = None
    p_seasons = a_seasons = 0
    p_w = p_l = p_gf = p_ga = p_og = p_ogo = p_a = p_ao = 0
    p_g = p_wpct = p_gs = p_go = p_gfg = p_gsg = p_gag = p_gog = p_ogg = 0
    a_w = a_l = a_gf = a_ga = a_og = a_ogo = a_a = a_ao = 0
    a_g = a_wpct = a_gs = a_go = a_gfg = a_gsg = a_gag = a_gog = a_ogg = 0
    p_g_2007 = a_g_2007 = 0
    
    def __init__(self, player):
        from models import PlayerLeagueBySeason
        self.season_stats = []
        self.player = player
        for season in PlayerLeagueBySeason.objects.filter(player=player,
                                                          league='P'
                                                          ).order_by('season__year'):
            s = SeasonStats(player, season.season)
            if len(s.week_stats) > 0:
                self.p_seasons += 1
                self.season_stats.append(s)
                self.p_w += s.w
                self.p_l += s.l
                self.p_gf += s.gf
                self.p_ga += s.ga
                self.p_og += s.og
                self.p_a += s.a
                if s.season.year > 2006:
                    self.p_g_2007 += s.w + s.l
                    self.p_ogo += s.ogo
                    self.p_ao += s.ao
                    self.p_gs += s.gs
                    self.p_gsg = g_rate(self.p_g_2007, self.p_gs)
        for season in PlayerLeagueBySeason.objects.filter(player=player,
                                                          league='A'
                                                          ).order_by('season__year'):
            s = SeasonStats(player, season.season)
            if len(s.week_stats) > 0:
                self.a_seasons += 1
                self.season_stats.append(s)
                self.a_w += s.w
                self.a_l += s.l
                self.a_gf += s.gf
                self.a_ga += s.ga
                self.a_og += s.og
                self.a_a += s.a
                if s.season.year > 2006:
                    self.a_g_2007 += s.w + s.l
                    self.a_ogo += s.ogo
                    self.a_ao += s.ao
                    self.a_gs += s.gs
                    self.a_gsg = g_rate(self.a_g_2007, self.a_gs)
        self.p_g = self.p_w + self.p_l
        self.p_wpct = win_pct(self.p_g, self.p_w)
        self.p_go = self.p_ga - self.p_og
        self.p_gfg = g_rate(self.p_g, self.p_gf)
        self.p_gsg = g_rate(1, self.p_gsg)
        self.p_gag = g_rate(self.p_g, self.p_ga)
        self.p_gog = g_rate(self.p_g, self.p_go)
        self.p_ogg = g_rate(self.p_g, self.p_og)
        self.a_g = self.a_w + self.a_l
        self.a_wpct = win_pct(self.a_g, self.a_w)
        self.a_go = self.a_ga - self.a_og
        self.a_gfg = g_rate(self.a_g, self.a_gf)
        self.a_gsg = g_rate(1, self.a_gsg)
        self.a_gag = g_rate(self.a_g, self.a_ga)
        self.a_gog = g_rate(self.a_g, self.a_go)
        self.a_ogg = g_rate(self.a_g, self.a_og)
        if self.p_g_2007 == 0:
            self.p_gs = self.p_ao = self.p_gsg = ' '
        if self.a_g_2007 == 0:
            self.a_gs = self.a_ao = self.a_gsg = ' '


class PostSeasonGameStats:
    player = None
    game = None
    opponent = None
    outcome = 'L'
    gf = ga = og = ogo = a = ao = 0
    gs = go = 0
    
    def __init__(self, player, game):
        from models import PostSeasonGamePre2008, PostSeasonGame
        if not game.player1 == player and not game.player2 == player:
            raise Exception(str(player) + ' is not in ' + str(game))
        self.player = player
        self.game = game
        if type(game) is PostSeasonGamePre2008:
            if game.player1 == player:
                self.opponent = game.player2
                self.gf = game.p1_gf
                self.ga = game.p2_gf
                self.og = game.p1_og
                self.ogo = game.p2_og
                self.a = game.p1_a
                self.ao = game.p2_a
                if game.winner() == 'p1':
                    self.outcome = 'W'
            else:
                self.opponent = game.player1
                self.gf = game.p2_gf
                self.ga = game.p1_gf
                self.og = game.p2_og
                self.ogo = game.p1_og
                self.a = game.p2_a
                self.ao = game.p1_a
                if game.winner() == 'p2':
                    self.outcome = 'W'
        elif type(game) is PostSeasonGame:
            pass # TODO: Crunch numbers for postseason games 2008+
        self.gs = self.gf - self.ogo
        self.go = self.ga - self.og


class PostSeasonSeriesStats:
    game_stats = None
    player = None
    series = ''
    season = None
    w = l = gf = ga = og = ogo = a = ao = 0
    g = wpct = gs = go = gfg = gsg = gag = gog = ogg = 0
    
    def __init__(self, player, series, season):
        from models import PostSeasonGamePre2008
        self.game_stats = []
        self.player = player
        self.series = series
        self.season = season
        if season.season.year < 2008:
            for game in PostSeasonGamePre2008.objects.filter(Q(player1=player) |
                                                             Q(player2=player),
                                                             postseason=season,
                                                             series=series,
                                                             ).order_by('game_num'):
                g = PostSeasonGameStats(player, game)
                self.game_stats.append(g)
                self.gf += g.gf
                self.ga += g.ga
                self.og += g.og
                self.ogo += g.ogo
                self.a += g.a
                self.ao += g.ao
                if g.outcome == 'W':
                    self.w += 1
                else:
                    self.l += 1
        else:
            pass # TODO: Crunch numbers for series 2008+
        self.g = self.w + self.l
        self.wpct = win_pct(self.g, self.w)
        self.gs = self.gf - self.ogo
        self.go = self.ga - self.og
        self.gfg = g_rate(self.g, self.gf)
        self.gsg = g_rate(self.g, self.gs)
        self.gag = g_rate(self.g, self.ga)
        self.gog = g_rate(self.g, self.go)
        self.ogg = g_rate(self.g, self.og)


class PostSeasonStats:
    series_stats = None
    player = None
    season = None
    w = l = gf = ga = og = ogo = a = ao = 0
    g = wpct = gs = go = gfg = gsg = gag = gog = ogg = 0
    
    def __init__(self, player, season):
        from models import SERIES_CHOICES
        self.series_stats = []
        self.player = player
        self.season = season
        for series in SERIES_CHOICES:
            s = PostSeasonSeriesStats(player, series[0], season)
            if len(s.game_stats) > 0:
                self.series_stats.append(s)
                self.w += s.w
                self.l += s.l
                self.gf += s.gf
                self.ga += s.ga
                self.og += s.og
                self.a += s.a
                self.ogo += s.ogo
                self.ao += s.ao
        self.g = self.w + self.l
        self.gs = self.gf - self.ogo
        self.go = self.ga - self.og
        self.wpct = win_pct(self.g, self.w)
        self.gfg = g_rate(self.g, self.gf)
        self.gsg = g_rate(self.g, self.gs)
        self.gag = g_rate(self.g, self.ga)
        self.gog = g_rate(self.g, self.go)
        self.ogg = g_rate(self.g, self.og)


class PostSeasonCareerStats:
    postseason_stats = None
    player = None
    w = l = gf = ga = og = ogo = a = ao = 0
    g = wpct = gs = go = gfg = gsg = gag = gog = ogg = 0
    
    def __init__(self, player):
        from models import PostSeason
        self.postseason_stats = []
        self.player = player
        for season in PostSeason.objects.filter(Q(pro_champ=player) |
                                                Q(pro2=player) |
                                                Q(ama_champ_or_pro3=player)
                                                ).order_by('season__year'):
            s = PostSeasonStats(player, season)
            if len(s.series_stats) > 0:
                self.postseason_stats.append(s)
                self.w += s.w
                self.l += s.l
                self.gf += s.gf
                self.ga += s.ga
                self.og += s.og
                self.a += s.a
                self.ogo += s.ogo
                self.ao += s.ao
                self.gs += s.gs
        self.g = self.w + self.l
        self.wpct = win_pct(self.g, self.w)
        self.go = self.ga - self.og
        self.gfg = g_rate(self.g, self.gf)
        self.gsg = g_rate(self.g, self.gs)
        self.gag = g_rate(self.g, self.ga)
        self.gog = g_rate(self.g, self.go)
        self.ogg = g_rate(self.g, self.og)
