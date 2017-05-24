import requests
import json
from loadprofile.models import Summoner, MatchSummary
def findSummoner(summonerName):
	r = requests.get("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")

	if r.status_code not in [200, 429]:
		raise ApiException(r.status_code)
	else: 
		jsonDict = r.json()
		s = Summoner(summoner_name = jsonDict['name'], account_id = jsonDict['accountId'], summoner_level = jsonDict['summonerLevel'], profile_icon_id = jsonDict['profileIconId'])
		s.save()
		return jsonDict['accountId']

def populateDatabases(accountId):
	populateMatches(accountId)

def populateMatches(accountId):
	r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+accountId+"?endIndex=5&beginIndex=0&api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
	if r.status_code not in [200, 429]:
		raise ApiException(r.status_code)
	else:
		matches = r.json()['matches']
		for match in matches:
			populateMatch(match['gameId'], accountId)
			
def populateMatch(gameId, accountId):
	try: 
		q = MatchSummary.objects.get(match_id=gameId, summoner=Summoner.objects.get(account_id=accountId))
	except MatchSummary.DoesNotExist:
		r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matches/"+str(gameId)+"?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
		participantId = 0
		if r.status_code not in [200, 404, 429]:
			raise ApiException(r.status_code)
		else:
			for participant in r.json()['participantIdentities']:
				if participant['player']['accountId'] == accountId:
					participantId = participant['participantId']
		participantDto = r.json()['participants'][participantId-1]
		timeline = participantDto['timeline']
		csPerMin = timeline['creepsPerMinDeltas']["0-10"]
		gpPerMin = timeline['goldPerMinDeltas']["0-10"]
		xpPerMin = timeline['xpPerMinDeltas']["0-10"]
		won = r.json()['teams'][0]['win'] == 'Win'
		if participantId > 5:
			won = not won
		ms = MatchSummary(match_id = gameId, win_loss = won, cs_average10 = csPerMin, gpm_average10 = gpPerMin, xpm_average10 = xpPerMin, summoner =Summoner.objects.get(account_id=accountId))
		print("matchAdded")
		ms.save()
			

class ApiException(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        
        if status_code == 404:
            self.exceptionType = "input"
            
        elif status_code == 429:
            self.exceptionType = "rate"
            
        elif status_code in [400, 401, 403, 405, 415, 500, 502, 503, 504]:
            self.exceptionType = "other"