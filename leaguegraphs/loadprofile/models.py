from django.db import models

# Create your models here.
#Summoner model, keeps track of latest date a Summoner's entries were modified, along with name, acc_id, profile_icon_id and level
class Summoner(models.Model):
    summoner_name = models.CharField(max_length=100)
    account_id = models.BigIntegerField()
    profile_icon_id = models.IntegerField()
    summoner_level = models.BigIntegerField()
    last_change = models.DateTimeField(auto_now=True)
    
    #method returns whether this entry has been updated in the last 15 minutes
    def was_published_recently(self):
        return self.last_change >= timezone.now() - datetime.timedelta(minutes = 15)
    
    def __str__(self):
        return '%s %d' % (self.summoner_name, self.account_id)

#provides a summary view of a match, from team 1's perspective with relevant query data
class MatchSummary(models.Model):
    match_id = models.BigIntegerField()
    #data for profile chart
    win_loss = models.BooleanField()
    cs_average10 = models.FloatField()
    gpm_average10 = models.FloatField()
    xpm_average10 = models.FloatField()
    game_date = models.BigIntegerField()
    # data for individual match summary
    role = models.CharField(max_length=100)
    champion = models.IntegerField()
    spell1 = models.IntegerField()
    spell2 = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    lvl = models.IntegerField()
    endGold = models.IntegerField()
    endCS = models.IntegerField()
    items = models.CharField(max_length=100)
    
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    
    def clear_old_games(account_id):
        query = MatchSummary.objects.filter(summoner=Summoner.objects.get(account_id=account_id)).order_by('game_date')
        cutoffindex = query.count() - 5
        datecutoff = query[cutoffindex].game_date
        deletequery = query.filter(game_date__lt=datecutoff)
        deletequery.delete()
            
        
    
    def __str__(self):
        return '%s, %d' % (self.summoner, self.match_id)    


    