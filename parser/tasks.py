# parser/tasks.py
import logging

from celery import shared_task
from django.core.cache import cache

from parser.Crawler import crawl_single_source
from sources.models import Source, Keyword

CACHE_TIMEOUT = 600

logger = logging.getLogger(__name__)


def get_cached_keywords():
    return cache.get_or_set(
        'crawler_keywords_list',
        lambda: [k.word.lower() for k in Keyword.objects.all()],
        timeout=CACHE_TIMEOUT
    )


#
# Парсинг одного конкретного источника
#
@shared_task(name="parser.tasks.celery_crawl_single_source")
def celery_crawl_single_source(source_id: int):
    try:
        source = Source.objects.get(pk=source_id, isActive=True)

        crawl_single_source(source, get_cached_keywords())

    except Source.DoesNotExist:
        logger.warning(f"Источник {source_id} не найден")
    except Exception as e:
        logger.exception(f"Ошибка при парсинге источника {source_id}: {e}")


#
# Роутер для Админки
# Задача для запуска парсинга нескольких источников по их ID.
#
@shared_task(name="parser.tasks.celery_crawl_sources_task")
def celery_crawl_sources_task(source_ids):
    sources = Source.objects.filter(pk__in=source_ids, isActive=True)
    for source in sources:
        celery_crawl_single_source.delay(source.id)


#
# Роутер для Beat и Кнопки
# Глобальная задача для запуска всех активных парсеров.
#
@shared_task(name="parser.tasks.celery_crawl_all_active_sources_task")
def celery_crawl_all_active_sources_task():
    active_sources = Source.objects.filter(isActive=True)
    for source in active_sources:
        celery_crawl_single_source.delay(source.id)
