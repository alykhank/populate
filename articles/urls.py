from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^auth/$', views.auth, name='auth'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^bookmarks/(?P<request_token>\w+)/(?P<request_token_secret>\w+)/(?P<oauth_verifier>\w+)$', views.bookmarks, name='bookmarks'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^twitter/login/$', views.twitter_login, name='twitter_login'),
	url(r'^twitter/success/$', views.twitter_success, name='twitter_success'),
)
