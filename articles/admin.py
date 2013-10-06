from django.contrib import admin

from articles.models import Article, Bookmark

class ArticleInline(admin.TabularInline):
	model = Article

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'excerpt', 'dek', 'word_count', 'date_published', 'url')

class BookmarkAdmin(admin.ModelAdmin):
	inlines = [ArticleInline]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
