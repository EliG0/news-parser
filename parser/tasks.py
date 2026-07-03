# parser/tasks.py
from celery import shared_task
from django.core.cache import cache
from sources.models import Source, Keyword
from parser.Crawler import crawl_single_source

CACHE_TIMEOUT = 600

def get_cached_keywords():
    return cache.get_or_set(
        'crawler_keywords_list',
        lambda: [k.word.lower() for k in Keyword.objects.all()],
        timeout=CACHE_TIMEOUT
    )


@shared_task
def celery_crawl_source_task(source_id):
    try:
        source = Source.objects.get(pk=source_id, isActive=True)

        keywords = get_cached_keywords()

        crawl_single_source(source, keywords)

    except Source.DoesNotExist:
        return f"Источник {source_id} не найден"