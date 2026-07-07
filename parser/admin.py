from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Article


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    list_display = ('title', "words", 'source', 'url', 'published_at', 'found_at',)
    list_filter = ('source', 'found_at', 'published_at')
    search_fields = ('title', 'text')
