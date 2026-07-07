import logging

from django.contrib import admin
from django.db.models import Count

from parser.models import Article
from parser.tasks import celery_crawl_sources_task
from .models import Source, Keyword

logger = logging.getLogger(__name__)
admin.site.register(Keyword)


@admin.action(description='🔄 Parse SELECTED sources')
def trigger_parser(modeladmin, request, queryset):
    logger.info(f"Triggering parser for {queryset.count()} sources")
    source_ids = list(queryset.values_list('id', flat=True))

    celery_crawl_sources_task.delay(source_ids)
    modeladmin.message_user(request, f"{queryset.count()} sources have been successfully submitted to Celery")


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0

    fields = ('title', 'found_at', 'words', "url")
    readonly_fields = ('title', 'found_at', 'words', 'url')
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-found_at')[:20]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'article_count', 'source_type', 'is_active', "patterns", "rss")
    list_filter = ('source_type', 'is_active')
    search_fields = ('name', 'url')
    actions = [trigger_parser]
    inlines = [ArticleInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(article_count=Count('articles'))

    @admin.display(ordering='article_count', description='Собрано статей')
    def article_count(self, obj):
        return obj.article_count