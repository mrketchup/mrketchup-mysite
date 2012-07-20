from django.db import models
from datetime import date
from common import years_between
from stats import CareerStats, PostSeasonCareerStats

HAND_CHOICES = (
    ('L', 'Left'),
    ('R', 'Right'),
    ('S', 'Switch'),
    ('U', 'Unknown'),
)

LEAGUE_CHOICES = (
    ('A', 'Ama'),
    ('P', 'Pro'),
)

CODE_CHOICES = (
    ('1A', 'Player One Ace'),
    ('2A', 'Player Two Ace'),
    ('1G', 'Player One Goal'),
    ('2G', 'Player Two Goal'),
    ('1OG', 'Player One Own Goal'),
    ('2OG', 'Player Two Own Goal'),
)

SERIES_CHOICES = (
    ('PCS', 'Pre Championship Series'),
    ('CS', 'Championship Series'),
)


################################################################################

class Player(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    hand = models.CharField("Handedness", max_length=1, choices=HAND_CHOICES)
    birth_date = models.DateField("Date of Birth", blank=True, null=True)
    death_date = models.DateField("Date of Death", blank=True, null=True)
    
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    full_name.short_description = 'Full Name'
    
    def is_alive(self):
        return not self.death_date
    
    def age(self, season=None):
        if season:
            return years_between(self.birth_date, date(season.year, 9, 1))
        elif not self.birth_date:
            return 'Unknown'
        else:
            endDate = date.today() if self.is_alive() else self.death_date
            return years_between(self.birth_date, endDate)
    age.short_description = 'Age'
    
    def career_stats(self):
        return CareerStats(self)
    
    def postseason_career_stats(self):
        return PostSeasonCareerStats(self)
        
    def __unicode__(self):
        return self.full_name()
    
################################################################################
    
class Season(models.Model):
    year = models.PositiveIntegerField("Year")
    
    def __unicode__(self):
        return str(self.year)
    
################################################################################
    
class PlayerLeagueBySeason(models.Model):
    player = models.ForeignKey(Player)
    season = models.ForeignKey(Season)
    league = models.CharField("League", max_length=1, choices=LEAGUE_CHOICES)
    
    class Meta:
        verbose_name = "Player League By Season"
        verbose_name_plural = "Player Leagues By Season"
    
################################################################################

class Week(models.Model):
    season = models.ForeignKey(Season)
    week_num = models.PositiveSmallIntegerField("Week")
    
    def __unicode__(self):
        return str(self.season) + "." + str(self.week_num)
    
################################################################################

class WeekPre2007(models.Model):
    week = models.ForeignKey(Week)
    player = models.ForeignKey(Player)
    og = models.PositiveSmallIntegerField("Own Goals")
    a = models.PositiveSmallIntegerField("Aces")
    
    class Meta:
        verbose_name = "Week Pre 2007"
        verbose_name_plural = "Weeks Pre 2007"
        
    def __unicode__(self):
        return str(self.week) + ": " + str(self.player)

################################################################################
    
class Game(models.Model):
    player1 = models.ForeignKey(Player, verbose_name='Player One',
                                related_name='game_player1')
    player2 = models.ForeignKey(Player, verbose_name='Player Two',
                                related_name='game_player2')
    week = models.ForeignKey(Week)
    date = models.DateTimeField("Date of Game")
    
    def __unicode__(self):
        return self.player1.full_name() + " v " + self.player2.full_name()
    
################################################################################

class GamePre2007(models.Model):
    player1 = models.ForeignKey(Player, verbose_name='Player One',
                                related_name='gamepre2007_player1')
    player2 = models.ForeignKey(Player, verbose_name='Player Two',
                                related_name='gamepre2007_player2')
    week = models.ForeignKey(Week)
    p1_gf = models.PositiveSmallIntegerField("P1 Goals For")
    p2_gf = models.PositiveSmallIntegerField("P2 Goals For")
    
    class Meta:
        verbose_name = "Game Pre 2007"
        verbose_name_plural = "Games Pre 2007"
        
    def winner(self):
        if self.p1_gf > self.p2_gf:
            return 'p1'
        return 'p2'
    
    def __unicode__(self):
        return self.player1.full_name() + " v " + self.player2.full_name()
    
################################################################################

class GamePre2010(models.Model):
    player1 = models.ForeignKey(Player, verbose_name='Player One',
                                related_name='gamepre2010_player1')
    player2 = models.ForeignKey(Player, verbose_name='Player Two',
                                related_name='gamepre2010_player2')
    week = models.ForeignKey(Week)
    p1_gf = models.PositiveSmallIntegerField("P1 Goals For")
    p2_gf = models.PositiveSmallIntegerField("P2 Goals For")
    p1_og = models.PositiveSmallIntegerField("P1 Own Goals")
    p2_og = models.PositiveSmallIntegerField("P2 Own Goals")
    p1_a = models.PositiveSmallIntegerField("P1 Aces")
    p2_a = models.PositiveSmallIntegerField("P2 Aces")
    
    class Meta:
        verbose_name = "Game Pre 2010"
        verbose_name_plural = "Games Pre 2010"
        
    def winner(self):
        if self.p1_gf > self.p2_gf:
            return 'p1'
        return 'p2'
    
    def __unicode__(self):
        return self.player1.full_name() + " v " + self.player2.full_name()
    
################################################################################
    
class Play(models.Model):
    game = models.ForeignKey(Game)
    code = models.CharField("Play Code", max_length=3, choices=CODE_CHOICES)
    time_stamp = models.DateTimeField("Time of Play")
    
################################################################################
    
class PostSeason(models.Model):
    season = models.ForeignKey(Season)
    pro_champ = models.ForeignKey(Player, verbose_name="Pro Champ",
                                  related_name='ps_pro_champ')
    pro2 = models.ForeignKey(Player, verbose_name="Pro Runner Up", 
                             related_name='ps_pro2')
    ama_champ_or_pro3 = models.ForeignKey(Player,
                                          verbose_name="Amateur Champ/3rd Pro",
                                          related_name='ps_ama_champ_pro3')
    
    def __unicode__(self):
        return str(self.season.year)
    
################################################################################

class PostSeasonGamePre2008(models.Model):
    player1 = models.ForeignKey(Player, verbose_name='Player One',
                                related_name='ps_gamepre2008_player1')
    player2 = models.ForeignKey(Player, verbose_name='Player Two',
                                related_name='ps_gamepre2008_player2')
    postseason = models.ForeignKey(PostSeason)
    series = models.CharField("Series", max_length=3, choices=SERIES_CHOICES)
    game_num = models.PositiveSmallIntegerField('Game')
    p1_gf = models.PositiveSmallIntegerField("P1 Goals For")
    p2_gf = models.PositiveSmallIntegerField("P2 Goals For")
    p1_og = models.PositiveSmallIntegerField("P1 Own Goals")
    p2_og = models.PositiveSmallIntegerField("P2 Own Goals")
    p1_a = models.PositiveSmallIntegerField("P1 Aces")
    p2_a = models.PositiveSmallIntegerField("P2 Aces")
    
    class Meta:
        verbose_name = "Post Season Game Pre 2008"
        verbose_name_plural = "Post Season Games Pre 2008"
        
    def winner(self):
        if self.p1_gf > self.p2_gf:
            return 'p1'
        return 'p2'
    
    def __unicode__(self):
        return self.player1.full_name() + " v " + self.player2.full_name()
    
################################################################################
    
class PostSeasonGame(models.Model):
    player1 = models.ForeignKey(Player, verbose_name='Player One',
                                related_name='ps_game_player1')
    player2 = models.ForeignKey(Player, verbose_name='Player Two',
                                related_name='ps_game_player2')
    postseason = models.ForeignKey(PostSeason)
    series = models.CharField("Series", max_length=3, choices=SERIES_CHOICES)
    game_num = models.PositiveSmallIntegerField('Game')
    date = models.DateTimeField("Date of Game")
    
    def __unicode__(self):
        return self.player1.full_name() + " v " + self.player2.full_name()
    
################################################################################
    
class PostSeasonPlay(models.Model):
    game = models.ForeignKey(PostSeasonGame)
    code = models.CharField("Play Code", max_length=3, choices=CODE_CHOICES)
    time_stamp = models.DateTimeField("Time of Play")
