from django.db import models
from django.contrib.auth.models import User

class TwitterProfile(models.Model):
	"""
		A Profile model that handles storing the oauth_token and
		oauth_secret in relation to a user.
	"""
	user = models.OneToOneField(User)
	oauth_token = models.CharField(max_length=200)
	oauth_token_secret = models.CharField(max_length=200)

class ReadabilityProfile(models.Model):
	"""
		A Profile model that handles storing the oauth_token and
		oauth_secret in relation to a user.
	"""
	user = models.OneToOneField(User)
	oauth_token = models.CharField(max_length=200)
	oauth_token_secret = models.CharField(max_length=200)

class Bookmark(models.Model):
	user = models.ForeignKey(User)
	readability_user_id = models.PositiveIntegerField(default=0)
	read_percent = models.FloatField(default=0.0)
	date_updated = models.DateTimeField(null=True, blank=True)
	favorite = models.BooleanField()
	# bookmark_id = models.PositiveIntegerField(default=0)
	date_archived = models.DateTimeField(null=True, blank=True)
	date_opened = models.DateTimeField(null=True, blank=True)
	date_added = models.DateTimeField(null=True, blank=True)
	article_href = models.CharField(max_length=500, null=True, blank=True)
	date_favorited = models.DateTimeField(null=True, blank=True)
	archive = models.BooleanField()
	# tags

	# def __unicode__(self):
	# 	return "<Bookmark('%s')>" % (self.bookmark_id)

class Article(models.Model):
	domain = models.CharField(max_length=500, null=True, blank=True)
	# next_page_href
	author = models.CharField(max_length=500, null=True, blank=True)
	url = models.URLField(null=True)
	lead_image_url = models.URLField(null=True)
	# content_size
	title = models.CharField(max_length=500, null=True, blank=True)
	excerpt = models.CharField(max_length=500, null=True, blank=True)
	word_count = models.PositiveIntegerField(default=0)
	content = models.TextField()
	date_published = models.DateTimeField(null=True, blank=True)
	dek = models.CharField(max_length=500, null=True, blank=True)
	# processed
	short_url = models.URLField(null=True)
	# article_id
	bookmark = models.ForeignKey(Bookmark)
	twitterLink = models.URLField()
	ideoLink = models.URLField()

	def __unicode__(self):
		return "<Article('%s', '%s')>" % (self.title, self.author)

class Alchemy(models.Model):
	article = models.ForeignKey(Article)
	concept = models.CharField(max_length=500)
	relevance = models.FloatField(0.0)

	def __unicode__(self):
		return self.concept

class Status(models.Model):
	article = models.ForeignKey(Article)
	text = models.CharField(max_length=200)
	user_name = models.CharField(max_length=200)
	user_image = models.URLField(null=True)
	user_screenname = models.CharField(max_length=200)
