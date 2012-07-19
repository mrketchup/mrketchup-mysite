from models import Player, Season, PlayerLeagueBySeason, Week, WeekPre2007, \
                    Game, GamePre2007, GamePre2010, Play, PostSeason, \
                    PostSeasonGamePre2008, PostSeasonGame, PostSeasonPlay
from django.contrib import admin

class PlayInline(admin.TabularInline):
    model = Play
    extra = 0
    
class PSPlayInline(admin.TabularInline):
    model = PostSeasonPlay
    extra = 0

class WeekInline(admin.TabularInline):
    model = Week
    extra = 0

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'hand', 'birth_date', 'death_date', 'age')
    search_fields = ['first_name', 'last_name']
    
class SeasonAdmin(admin.ModelAdmin):
    inlines = [WeekInline]
    
class PlayerLeagueBySeasonAdmin(admin.ModelAdmin):
    list_display = ('player', 'league', 'season')

class WeekPre2007Admin(admin.ModelAdmin):
    list_display = ('week', 'player', 'og', 'a')
    
class GameAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'week', 'date')
    inlines = [PlayInline]
    
class GamePre2007Admin(admin.ModelAdmin):
    list_display = ('__unicode__', 'week', 'p1_gf', 'p2_gf')
    
class GamePre2010Admin(admin.ModelAdmin):
    list_display = ('__unicode__', 'week', 'p1_gf', 'p2_gf')
    
class PostSeasonAdmin(admin.ModelAdmin):
    list_display = ('season', 'pro_champ', 'pro2', 'ama_champ_or_pro3')

class PostSeasonGamePre2008Admin(admin.ModelAdmin):
    list_display = ('__unicode__', 'postseason', 'series', 'game_num', 'p1_gf', 'p2_gf')

class PostSeasonGameAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'postseason', 'series', 'game_num', 'date')
    inlines = [PSPlayInline]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(PlayerLeagueBySeason, PlayerLeagueBySeasonAdmin)
admin.site.register(WeekPre2007, WeekPre2007Admin)
admin.site.register(Game, GameAdmin)
admin.site.register(GamePre2007, GamePre2007Admin)
admin.site.register(GamePre2010, GamePre2010Admin)
admin.site.register(PostSeason, PostSeasonAdmin)
admin.site.register(PostSeasonGamePre2008, PostSeasonGamePre2008Admin)
admin.site.register(PostSeasonGame, PostSeasonGameAdmin)
