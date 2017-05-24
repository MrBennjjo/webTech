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
	win_loss = models.BooleanField()
	end_golddifference = models.IntegerField()
	biggest_deficit = models.IntegerField(default=0)
	biggest_advantage = models.IntegerField(default=0)
	
	def __str__(self):
		return '%d' % (self.match_id)	

#join table between summoner and match
class SummonerMatch(models.Model):
	match = models.ForeignKey(MatchSummary, on_delete=models.CASCADE)
	summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
	participant_id = models.IntegerField()
	
	def __str__(self): 
		return 'Match: %d, Summoner %d, Team %d' % (self.match, self.summoner, self.team_id)
	
class ProfileQueries(models.Model): 
	summoner = models.ForeignKey(account_id, 