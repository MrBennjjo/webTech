from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from loadprofile.util import findSummoner, ApiException
# Create your views here.

def base(request):
    return HttpResponseRedirect(reverse('loadprofile:home'))

def home(request):
    return render(request, 'loadprofile/home.html')

def form(request):
    postName = request.POST['summonerName']
    
    try:
        accountId = findSummoner(postName)
        return HttpResponseRedirect(reverse('loadprofile:profile', args = [accountId]))
    except ApiException:
        return render(request, 'loadprofile/home.html', {'error_message': "You didn't select a choice.",})

def profile(request, accountId):
    return render(request, 'loadprofile/profile.html', {'accountId': accountId,})
