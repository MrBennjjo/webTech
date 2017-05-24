from django.conf.urls import url

from . import views

app_name = 'loadprofile'
urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^home$', views.home, name='home'),
	url(r'^form$', views.form, name='form'),
    url(r'^profile/(?P<accountId>[0-9]+)$', views.profile, name='profile'),
]