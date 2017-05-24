import requests
import json

def findSummoner(summonerName):
    r = requests.get("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
    
    if r.status_code != 200:
        raise ApiException(r.status_code)
    else: 
        jsonDict = r.json()
        return jsonDict['accountId']
        
class ApiException(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        
        if status_code == 404:
            self.exceptionType = "input"
            
        elif status_code == 429:
            self.exceptionType = "rate"
            
        elif status_code in [400, 401, 403, 405, 415, 500, 502, 503, 504]:
            self.exceptionType = "other"