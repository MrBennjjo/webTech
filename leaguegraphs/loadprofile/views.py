from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from loadprofile.util import findSummoner,populateDatabases, ApiException
from loadprofile.models import Summoner
# Create your views here.


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
			populateDatabases(accountId)
			print("Used API")
			return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
		except ApiException as errormess:
			return render(request, 'loadprofile/home.html', {'error_message': "Error of type " + errormess.exceptionType,})	
	
    

def profile(request, accountId):
    return render(request, 'loadprofile/profile.html', {'accountId': accountId, 'comeback_value': "10 golden pennies", 'throw_value': "a mars bar",})
