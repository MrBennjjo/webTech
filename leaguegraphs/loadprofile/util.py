import requests
import json
import time
from loadprofile.models import Summoner, MatchSummary
def findSummoner(summonerName):
    r = limitedRequest("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")

    if r.status_code not in [200, 429]:
        raise ApiException(r.status_code, "Invalid name entered or API server issue")
    else: 
        jsonDict = r.json()
        s = Summoner(summoner_name = jsonDict['name'], account_id = jsonDict['accountId'], summoner_level = jsonDict['summonerLevel'], profile_icon_id = jsonDict['profileIconId'])
        s.save()
        
        return jsonDict['accountId']

def populateDatabases(accountId):
    populateMatches(accountId)

def populateMatches(accountId):
    r = limitedRequest("https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+accountId+"?queue=440&queue=420&queue=410&endIndex=10&beginIndex=0&api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
    if r.status_code not in [200, 429, 404]:
        raise ApiException(r.status_code, "Server error")
    elif r.status_code == 404:
        raise ApiException(r.status_code, "0 ranked games played")
    else:
        matches = r.json()['matches']
        if len(matches) < 5 :
            raise ApiException(404, "Played too few ranked games")
        matchAdded =0
        i = 0
        while matchAdded < 5 and i < len(matches):
            if populateMatch(matches[i]['gameId'], accountId): 
                matchAdded += 1
            i += 1
        if i==9:
            raise ApiException(404, "Unexpected data in last 10 games")
        else:
            MatchSummary.clear_old_games(accountId);
            
def populateMatch(gameId, accountId):
    try: 
        MatchSummary.objects.get(match_id=gameId, summoner=Summoner.objects.get(account_id=accountId))
        return True
    except MatchSummary.DoesNotExist:
        r = limitedRequest("https://euw1.api.riotgames.com/lol/match/v3/matches/"+str(gameId)+"?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
        try:
            longDate = int(r.json()['gameCreation'])
            participantIndex = 0
            if r.status_code not in [200, 404, 429]:
                raise ApiException(r.status_code, "Server error")
            else:
                for i in range(0, 10):
                    if str(r.json()['participantIdentities'][i]['player']['accountId']) == str(accountId):
                        participantIndex = i
            timeline = r.json()['participants'][participantIndex]['timeline']
            csPerMin = timeline['creepsPerMinDeltas']["0-10"]
            gpPerMin = timeline['goldPerMinDeltas']["0-10"]
            xpPerMin = timeline['xpPerMinDeltas']["0-10"]
            won = r.json()['teams'][0]['win'] == 'Win'
            if participantIndex > 4:
                won = not won
                
            role = timeline['lane']
            if role == "BOTTOM":
                role = timeline['role'][4:]
            
            champion = r.json()['participants'][participantIndex]['championId'];
            spell1  = r.json()['participants'][participantIndex]['spell1Id'];
            spell2  = r.json()['participants'][participantIndex]['spell2Id'];
            
            stats = r.json()['participants'][participantIndex]['stats']
            kills  = stats['kills'];
            deaths  = stats['deaths'];
            assists  = stats['assists'];
            
            lvl  = stats['champLevel'];
            endCS  = stats['totalMinionsKilled'];
            endGold  = stats['goldEarned'];
            items = "%d,%d,%d,%d,%d,%d,%d" % (stats['item0'], stats['item1'], stats['item2'], stats['item3'], stats['item4'],  stats['item5'], stats['item6'])
            
            ms = MatchSummary(match_id=gameId, game_date=longDate, win_loss=won, cs_average10=csPerMin, gpm_average10=gpPerMin, xpm_average10=xpPerMin, summoner=Summoner.objects.get(account_id=accountId), role=role, champion=champion, spell1=spell1, spell2=spell2, kills=kills, deaths=deaths, assists=assists, lvl=lvl, endCS=endCS, endGold=endGold, items=items)
            ms.save()
            return True
            
        except KeyError:
            return False

def getVersion():

    r = limitedRequest("https://euw1.api.riotgames.com/lol/static-data/v3/realms?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
    if r.status_code != 200:
        return "7.10.1"
    else:
        return r.json()["dd"]
            
def getChampData():
    r = limitedRequest("https://global.api.riotgames.com/api/lol/static-data/EUW/v1.2/champion?champData=info&dataById=true&api_key=RGAPI-7eb2d46e-20fc-48b2-8331-9fb6cb3a5dc7")
    
    return r.json()['data']
        
def limitedRequest(requestContent):
    success = False
    while success == False:
        r = requests.get(requestContent)
        if r.status_code == 429:
            waitTime = int(r.headers['Retry-after'])
            time.sleep(waitTime)
        else: success = True
    return r
    
    

class ApiException(Exception):

    def __init__(self, status_code, exceptionType):
        self.status_code = status_code
        self.exceptionType = exceptionType