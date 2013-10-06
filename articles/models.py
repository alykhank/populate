from django.db import models

class Bookmark(models.Model):
	user_id = models.PositiveIntegerField(default=0)
	read_percent = models.FloatField(default=0.0)
	date_updated = models.DateTimeField(null=True, blank=True)
	favorite = models.BooleanField()
	bookmark_id = models.PositiveIntegerField(default=0)
	date_archived = models.DateTimeField(null=True, blank=True)
	date_opened = models.DateTimeField(null=True, blank=True)
	date_added = models.DateTimeField(null=True, blank=True)
	article_href = models.CharField(max_length=200)
	date_favorited = models.DateTimeField(null=True, blank=True)
	archive = models.BooleanField()
	# tags

	def __unicode__(self):
		return "<Bookmark('%s')>" % (self.bookmark_id)

class Article(models.Model):
	domain = models.CharField(max_length=200)
	# next_page_href
	author = models.CharField(max_length=200)
	url = models.URLField()
	lead_image_url = models.URLField()
	# content_size
	title = models.CharField(max_length=200)
	excerpt = models.CharField(max_length=200)
	word_count = models.PositiveIntegerField(default=0)
	content = models.TextField()
	date_published = models.DateTimeField(null=True, blank=True)
	dek = models.CharField(max_length=200)
	# processed
	short_url = models.URLField()
	# article_id
	bookmark = models.ForeignKey(Bookmark)

	def __unicode__(self):
		return "<Article('%s', '%s')>" % (self.title, self.author)
