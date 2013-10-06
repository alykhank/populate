from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^auth/$', views.auth, name='auth'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^bookmarks/(?P<request_token>\w+)/(?P<request_token_secret>\w+)/(?P<oauth_verifier>\w+)$', views.bookmarks, name='bookmarks'),
)
