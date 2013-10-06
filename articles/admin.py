from django.contrib import admin

from articles.models import Bookmark, Article, Alchemy, Status

class ArticleInline(admin.TabularInline):
	model = Article

class BookmarkAdmin(admin.ModelAdmin):
	inlines = [ArticleInline]

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'excerpt', 'dek', 'word_count', 'date_published', 'url')

admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Alchemy)
admin.site.register(Status)
