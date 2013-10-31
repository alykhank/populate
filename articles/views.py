import os, json, urlparse
import requests
from rauth import OAuth1Service
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User

from articles.models import Bookmark, Article, Alchemy, Status

twitter = OAuth1Service(
	name = 'twitter',
	consumer_key = os.environ.get('TWITTER_CONS_KEY'),
	consumer_secret = os.environ.get('TWITTER_CONS_SECRET'),
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	authorize_url = 'https://api.twitter.com/oauth/authorize',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	base_url = 'https://api.twitter.com/'
)

readability = OAuth1Service(
	consumer_key=os.environ.get('CONS_KEY'),
	consumer_secret=os.environ.get('CONS_SECRET'),
	name='readability',
	request_token_url='https://www.readability.com/api/rest/v1/oauth/request_token/',
	authorize_url='https://www.readability.com/api/rest/v1/oauth/authorize/',
	access_token_url='https://www.readability.com/api/rest/v1/oauth/access_token/',
	base_url='https://www.readability.com/api/rest/v1/'
)

def logout(request):
	django_logout(request)
	messages.success(request, 'Successfully logged out.')
	return HttpResponseRedirect(reverse('articles:index'))

def twitter_login(request):
	request_token = twitter.get_raw_request_token(params={'oauth_callback': request.build_absolute_uri(reverse('articles:twitter_success'))})
	if request_token.status_code != 200:
		return twitter_login_failed(request)
	r = urlparse.parse_qs(request_token.text)
	if not r['oauth_callback_confirmed'][0]:
		return twitter_login_failed(request)
	request.session['request_token'] = r['oauth_token'][0]
	request.session['request_token_secret'] = r['oauth_token_secret'][0]
	return HttpResponseRedirect(twitter.base_url + 'oauth/authenticate?oauth_token=' + request.session['request_token'])

def twitter_login_failed(request):
	messages.error(request, 'Twitter login failed.')
	return HttpResponseRedirect(reverse('articles:index'))

def twitter_success(request):
	oauth_token = request.GET.get('oauth_token')
	oauth_verifier = request.GET.get('oauth_verifier')
	if 'request_token' in request.session and 'request_token_secret' in request.session:
		request_token = request.session['request_token']
		request_token_secret = request.session['request_token_secret']
		if request_token != oauth_token:
			return twitter_login_failed(request)
		access_token = twitter.get_raw_access_token(request_token, request_token_secret, params={'oauth_verifier': oauth_verifier})
		if access_token.status_code != 200:
			return twitter_login_failed(request)
		r = urlparse.parse_qs(access_token.text)
		oauth_token = r['oauth_token'][0]
		request.session['access_token'] = oauth_token
		oauth_token_secret = r['oauth_token_secret'][0]
		request.session['access_token_secret'] = oauth_token_secret
		request.session['user_id'] = r['user_id'][0]
		screen_name = r['screen_name'][0]
		request.session['screen_name'] = screen_name
		del request.session['request_token']
		del request.session['request_token_secret']

		try:
			user = User.objects.get(username=screen_name)
		except:
			user = User.objects.create_user(screen_name, None, oauth_token_secret)
			profile = TwitterProfile(user=user, oauth_token=oauth_token, oauth_token_secret=oauth_token_secret, screen_name=screen_name)
			profile.save()

		user = authenticate(username=screen_name, password=oauth_token_secret)
		if user is not None and user.is_active:
			login(request, user)
			messages.success(request, 'Logged in as ' + user.username + '.')
			return HttpResponseRedirect(reverse('articles:index'))
		else:
			messages.error(request, 'Invalid login.')
			return HttpResponseRedirect(reverse('articles:index'))

		messages.success(request, 'Logged in with Twitter as ' + request.session['screen_name'] + '.')
		return HttpResponseRedirect(reverse('articles:index'))
	else:
		return twitter_login_failed(request)

class IndexView(generic.ListView):
	template_name = 'articles/index.html'
	context_object_name = 'bookmark_list'

	def get_queryset(self):
		return Article.objects.all()

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
	bookmarks = session.get('bookmarks').content
	bkmkjson = json.loads(bookmarks)
	for b in bkmkjson['bookmarks']:
		bookmark = Bookmark(user_id=b['user_id'], read_percent=b['read_percent'], date_updated=b['date_updated'], favorite=b['favorite'], date_archived=b['date_archived'], date_opened=b['date_opened'], date_added=b['date_added'], article_href=b['article_href'], date_favorited=b['date_favorited'], archive=b['archive'])
		bookmark.save()
		r = session.get('articles/' + b['article']['id']).content
		a = json.loads(r)
		article = Article(domain=a['domain'], author=a['author'], url=a['url'], lead_image_url=a['lead_image_url'], title=a['title'], excerpt=a['excerpt'], word_count=a['word_count'], content=a['content'], date_published=a['date_published'], dek=a['dek'], short_url=a['short_url'], bookmark=bookmark)
		article.save()
		text = requests.post('http://access.alchemyapi.com/calls/url/URLGetText', data={'apikey': os.environ.get('ALCHEMY_API_KEY'), 'url': a['url'], 'outputMode': 'json'}).content
		conceptsResponse = requests.post('http://access.alchemyapi.com/calls/text/TextGetRankedConcepts', data={'apikey': os.environ.get('ALCHEMY_API_KEY'), 'text': text, 'outputMode': 'json'}).content
		conceptsJson = json.loads(conceptsResponse)
		for c in conceptsJson['concepts']:
			concept = Alchemy(article=article, concept=c['text'], relevance=c['relevance'])
			concept.save()
		concepts = []
		for concept in Alchemy.objects.filter(article=article):
			concepts.append(concept.concept)
		twitterConcepts = concepts[:3]
		conceptString = ('+').join(twitterConcepts)
		article.twitterLink = 'https://twitter.com/search' + '?q=' + conceptString
		ideoConcepts = concepts[:1]
		conceptString = ('+').join(ideoConcepts)
		article.ideoLink = 'http://www.openideo.com/search.html' + '?text=' + conceptString
		article.save()
	bookmark_list = Article.objects.all()
	return render(request, 'articles/index.html', {'bookmark_list': bookmark_list})
