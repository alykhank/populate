from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from articles.models import Bookmark, Article

class IndexView(generic.ListView):
	template_name = 'articles/index.html'

	def get_queryset(self):
		return Bookmark.objects.all()
