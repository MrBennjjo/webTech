from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.core import serializers
from loadprofile.util import findSummoner, populateDatabases, ApiException
from loadprofile.models import Summoner, MatchSummary

def base(request):
    return HttpResponseRedirect(reverse('loadprofile:home'))

def home(request):
    return render(request, 'loadprofile/home.html')

def form(request):
	postName = request.POST['summonerName']
	try:
		accountId = Summoner.objects.get(summoner_name__iexact=postName).account_id
		print("Used Database")
		return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
	except Summoner.DoesNotExist:
		try:
			accountId = findSummoner(postName)
			print("Used API")
			return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
		except ApiException as errormess:				
			return render(request, 'loadprofile/home.html', {'error_message': "Error of type " + errormess.exceptionType,})	
	
    

def profile(request, accountId):
	try:
		populateDatabases(accountId)
	except ApiException as errormess:
		return render(request, 'loadprofile/home.html', {'error_message': "Error of type " + errormess.exceptionType,})	
	return render(request, 'loadprofile/profile.html', {'accountId': accountId, 'comeback_value': "10 golden pennies", 'throw_value': "a mars bar",})

def getProfileData(request, accountId):
    q = MatchSummary.objects.filter(summoner=Summoner.objects.get(account_id=accountId))
    response = JsonResponse(list(q.values()), safe=False)
    
    return response