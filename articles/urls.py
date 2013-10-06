from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^auth/$', views.auth, name='auth'),
)
