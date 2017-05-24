import requests
import json
from loadprofile.models import Summoner, MatchSummary
class ApiCalls:
	apikey = "?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f"
	def findSummoner(summonerName):
		r = requests.get("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + apikey)

		if r.status_code not in [200, 429]:
			raise ApiException(r.status_code)
		else: 
			jsonDict = r.json()
			s = Summoner(summoner_name = jsonDict['name'], account_id = jsonDict['accountId'], summoner_level = jsonDict['summonerLevel'], profile_icon_id = jsonDict['profileIconId'])
			s.save()
			return jsonDict['accountId']

	def populateDatabases(accountId):
		populateMatches(accountId)
		runQueries(accountId)

	def populateMatches(accountId):
		r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+accountId+"/recent"+apikey)
		
		if r.status_code not in [200, 429]:
			raise ApiException(r.status_code)
		else:
			matches = r.json()['matches']
			for match in matches:
				populateMatch(match['gameId'], accountId)
			
	def populateMatch(gameId, accountId):
		r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matches/"+gameId+apikey)
		
		if r.status_code not in [200, 429]:
			raise ApiException(r.status_code)
		else:
			for participant in r.json()['participantIdentities']
				if participant['player']['accountId'] == accountId:
					participantId = participant['participantId']
					if participantId <= 5:
						teamId = 100
					else:
						teamId = 200
			if teamId == 100:
				
			
		
		

class ApiException(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        
        if status_code == 404:
            self.exceptionType = "input"
            
        elif status_code == 429:
            self.exceptionType = "rate"
            
        elif status_code in [400, 401, 403, 405, 415, 500, 502, 503, 504]:
            self.exceptionType = "other"