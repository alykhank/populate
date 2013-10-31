from django.contrib import admin

from articles.models import Bookmark, Article, Alchemy, Status, TwitterProfile, ReadabilityProfile

class ArticleInline(admin.TabularInline):
	model = Article

class BookmarkAdmin(admin.ModelAdmin):
	inlines = [ArticleInline]

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'excerpt', 'dek', 'word_count', 'date_published', 'url')

class TwitterProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)

class ReadabilityProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)

admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Alchemy)
admin.site.register(Status)
admin.site.register(TwitterProfile, TwitterProfileAdmin)
admin.site.register(ReadabilityProfile, ReadabilityProfileAdmin)
