from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import os
from rauth import OAuth1Service

from articles.models import Bookmark, Article

readability = OAuth1Service(
	consumer_key=os.environ.get('CONS_KEY'),
	consumer_secret=os.environ.get('CONS_SECRET'),
	name='readability',
	request_token_url='https://www.readability.com/api/rest/v1/oauth/request_token/',
	authorize_url='https://www.readability.com/api/rest/v1/oauth/authorize/',
	access_token_url='https://www.readability.com/api/rest/v1/oauth/access_token/',
	base_url='https://www.readability.com/api/rest/v1/'
)

class IndexView(generic.ListView):
	template_name = 'articles/index.html'

	def get_queryset(self):
		return Bookmark.objects.all()

def auth(request):
	redirect_uri = 'http://populate-mit.herokuapp.com/auth'
	request_token, request_token_secret = readability.get_request_token()
	url = readability.get_authorize_url(request_token, data={'oauth_callback': redirect_uri})
	return render(request, 'articles/auth.html', {'request_token': request_token, 'request_token_secret': request_token_secret, 'oauth_url': url})

def submit(request):
	try:
		request_token = request.POST['request_token']
		request_token_secret = request.POST['request_token_secret']
		oauth_verifier = request.POST['verification']
	except (KeyError):
		return render(request, 'articles/index.html')
	else:
		return HttpResponseRedirect(reverse('articles:bookmarks', kwargs={'request_token': request_token, 'request_token_secret': request_token_secret, 'oauth_verifier': oauth_verifier}))

def bookmarks(request, request_token, request_token_secret, oauth_verifier):
	session = readability.get_auth_session(request_token, request_token_secret, data={'oauth_verifier': oauth_verifier})
	return HttpResponse(session.get('bookmarks'))

