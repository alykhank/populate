from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import os, json
import requests
from rauth import OAuth1Service

from articles.models import Bookmark, Article, Alchemy, Status

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
