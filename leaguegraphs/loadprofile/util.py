import requests

def findSummoner(summonerName):
    r = requests.get("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=f083d3c8-2600-454b-ba0d-ac25bf9f5a1f")
    
    if r.status_code == 200:
        return True
    else: 
        return False