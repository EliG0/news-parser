# parser/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Article


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    list_display = ('title', 'source', 'foundAt', 'url', "words")
    list_filter = ('source', 'foundAt')
    search_fields = ('title', 'text')
