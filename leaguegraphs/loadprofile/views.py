from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.core import serializers
from loadprofile.util import findSummoner, populateDatabases, getVersion, getChampData, ApiException
from loadprofile.models import Summoner, MatchSummary

def base(request):
    return HttpResponseRedirect(reverse('loadprofile:home'))

def home(request):
    return render(request, 'loadprofile/home.html')

def form(request):
    postName = request.POST['summonerName']
    try:
        accountId = Summoner.objects.get(summoner_name__iexact=postName).account_id
        return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
    except Summoner.DoesNotExist:
        try:
            accountId = findSummoner(postName)
            return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
        except ApiException as errormess:                
            return render(request, 'loadprofile/home.html', {'error_message': errormess.exceptionType,})    
    
def profile(request, accountId):
    try:
        populateDatabases(accountId)
    except ApiException as errormess:
        return render(request, 'loadprofile/home.html', {'error_message': errormess.exceptionType,})    
    profile_icon = get_object_or_404(Summoner, account_id = accountId).profile_icon_id
    summoner_name = get_object_or_404(Summoner, account_id = accountId).summoner_name
    return render(request, 'loadprofile/profile.html', {'accountId': accountId, 'profile_icon': profile_icon , 'summoner_name': summoner_name,})

def getProfileData(request, accountId):
    q = MatchSummary.objects.filter(summoner=Summoner.objects.get(account_id=accountId))
    version = getVersion()
    champData = getChampData()
    qList = list(q.values())
    qList.append(version)
    qList.append(champData)
    
    
    response = JsonResponse(qList, safe=False)
    
    return response