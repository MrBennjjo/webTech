from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^home$', views.home, name='home'),
    #url(r'^$', views.profile, name='profile'),
]