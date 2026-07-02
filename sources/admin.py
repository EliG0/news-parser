from django.contrib import admin

from .models import Source, Keyword

admin.site.register(Keyword)

from django.contrib import admin
from parser.Crawler import ParserRun


@admin.action(description='🔄 Parse CURRENT sources')
def trigger_parser(modeladmin, request, queryset):
    ParserRun(sources_queryset=queryset)
    modeladmin.message_user(request, f"Success with {queryset.count()} sources")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sourceType', 'isActive', "patterns", "rss")
    list_filter = ('sourceType', 'isActive')
    search_fields = ('name', 'url')
    actions = [trigger_parser]
