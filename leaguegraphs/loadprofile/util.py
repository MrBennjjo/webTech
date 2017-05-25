import requests
import json
import time
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
    r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+accountId+"?queue=440&queue=420&queue=410&endIndex=10&beginIndex=0&api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
    if r.status_code not in [200, 429]:
        raise ApiException(r.status_code)
    else:
        matches = r.json()['matches']
        if len(matches) < 5 :
            raise ApiException(404)
        matchAdded =0
        i = 0
        while matchAdded < 5 and i < len(matches):
            if populateMatch(matches[i]['gameId'], accountId): 
                matchAdded += 1
            i += 1
        if i==9:
            raise ApiException(404)
            
def populateMatch(gameId, accountId):
    try: 
        MatchSummary.objects.get(match_id=gameId, summoner=Summoner.objects.get(account_id=accountId))
        return True
    except MatchSummary.DoesNotExist:
        r = requests.get("https://euw1.api.riotgames.com/lol/match/v3/matches/"+str(gameId)+"?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
        try:
            longDate = int(r.json()['gameCreation'])/1000

            print("this somehow worked")
            dateTimeStruct = time.gmtime(longDate)
            print("struct is fine")
            dateTime = time.strftime('%d/%m/%Y\n%H:%M', dateTimeStruct)
            participantIndex = 0
            if r.status_code not in [200, 404, 429]:
                raise ApiException(r.status_code)
            else:
                for i in range(0, 10):
                    if str(r.json()['participantIdentities'][i]['player']['accountId']) == str(accountId):
                        participantIndex = i
                        print(participantIndex)

            timeline = r.json()['participants'][participantIndex]['timeline']
            csPerMin = timeline['creepsPerMinDeltas']["0-10"]
            gpPerMin = timeline['goldPerMinDeltas']["0-10"]
            xpPerMin = timeline['xpPerMinDeltas']["0-10"]
            won = r.json()['teams'][0]['win'] == 'Win'
            if participantIndex > 4:
                won = not won
            ms = MatchSummary(match_id = gameId, game_date = dateTime, win_loss = won, cs_average10 = csPerMin, gpm_average10 = gpPerMin, xpm_average10 = xpPerMin, summoner =Summoner.objects.get(account_id=accountId))
            ms.save()
            return True
            
        except KeyError:
            return False
        

class ApiException(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        
        if status_code == 404:
            self.exceptionType = "input"
            
        elif status_code == 429:
            self.exceptionType = "rate"
            
        elif status_code in [400, 401, 403, 405, 415, 500, 502, 503, 504]:
            self.exceptionType = "other"