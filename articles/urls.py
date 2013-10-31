from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^bookmarks/(?P<request_token>\w+)/(?P<request_token_secret>\w+)/(?P<oauth_verifier>\w+)$', views.bookmarks, name='bookmarks'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^twitter/login/$', views.twitter_login, name='twitter_login'),
	url(r'^twitter/success/$', views.twitter_success, name='twitter_success'),
	url(r'^readability/login/$', views.readability_login, name='readability_login'),
	url(r'^readability/success/$', views.readability_success, name='readability_success'),
	url(r'^readability/unlink/$', views.readability_unlink, name='readability_unlink'),
)
