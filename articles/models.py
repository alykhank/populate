from django.db import models

class Bookmark(models.Model):
	user_id = models.PositiveIntegerField(default=0)
	read_percent = models.FloatField(default=0.0)
	date_updated = models.DateTimeField()
	favorite = models.BooleanField()
	bookmark_id = models.PositiveIntegerField(default=0)
	date_archived = models.DateTimeField()
	date_opened = models.DateTimeField()
	date_added = models.DateTimeField()
	article_href = models.CharField(max_length=200)
	date_favorited = models.DateTimeField()
	archive = models.BooleanField()
	# tags

	def __unicode__(self):
		return "<Bookmark('%s', '%s')>" % (self.bookmark_id, self.article.title)

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
	date_published = models.DateTimeField()
	dek = models.CharField(max_length=200)
	# processed
	short_url = models.URLField()
	# article_id
	bookmark = models.OneToOneField(Bookmark)

	def __unicode__(self):
		return "<Article('%s', '%s')>" % (self.title, self.author)
