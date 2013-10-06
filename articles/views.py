from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import os
from rauth import OAuth1Service

from articles.models import Bookmark, Article

class IndexView(generic.ListView):
	template_name = 'articles/index.html'

	def get_queryset(self):
		return Bookmark.objects.all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(IndexView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['auth_url'] = reverse('articles:auth')
		return context

def auth(request):
	readability = OAuth1Service(
		consumer_key=os.environ.get('CONS_KEY'),
		consumer_secret=os.environ.get('CONS_SECRET'),
		name='readability',
		request_token_url='https://www.readability.com/api/rest/v1/oauth/request_token/',
		authorize_url='https://www.readability.com/api/rest/v1/oauth/authorize/',
		access_token_url='https://www.readability.com/api/rest/v1/oauth/access_token/',
		base_url='https://www.readability.com/api/rest/v1/'
	)

	redirect_uri = 'http://populate-mit.herokuapp.com/auth'
	request_token, request_token_secret = readability.get_request_token()
	url = readability.get_authorize_url(request_token, data={'oauth_callback': redirect_uri})
	return HttpResponseRedirect(url)
