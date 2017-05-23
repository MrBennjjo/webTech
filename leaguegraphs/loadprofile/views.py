from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

# Create your views here.
def base(request):
    return HttpResponseRedirect(reverse('home'))

def home(request):
    return render(request, 'loadprofile/home.html')
    
def form(request):
    return HttpResponse("You're at form blah.")
    
def profile(request):
    return HttpResponse("You're at the profile.")
    