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


@shared_task(name="parser.tasks.celery_crawl_single_source")
def celery_crawl_single_source(source_id: int):
    """
        Основная задача Celery для парсинга ОДНОГО источника.

        Зачем здесь source_id:
        1. Сбой для одного источника не ломает весь процесс для других.
        2. Целери распределяет эти задачи по разным воркерам для одновременного запуска.
        3. Целери сереализует аргументы в JSON для передачи в Редис, но Django-модели напрямую не сереализуются.
        Даже если бы и сереализовались, то во-первых это было бы неэффективно, а во-вторых, данные могли бы устареть к моменту выполнения задачи.
        Поэтому передается только (примитив) во избежание проблем с сериализацией Django-моделей и устареванием данных.
    """
    try:
        source = Source.objects.get(pk=source_id, isActive=True)

        crawl_single_source(source, get_cached_keywords())

    except Source.DoesNotExist:
        logger.warning(f"Источник {source_id} не найден")
    except Exception as e:
        logger.exception(f"Ошибка при парсинге источника {source_id}: {e}")


@shared_task(name="parser.tasks.celery_crawl_sources_task")
def celery_crawl_sources_task(source_ids):
    """
        Задача-роутер. Принимает список ID из админ-панели (Django bulk action)
        и дробит их на множество независимых параллельных подзадач celery_crawl_single_source.
    """
    s_ids = Source.objects.filter(pk__in=source_ids, isActive=True).values_list('id', flat=True)
    for s_id in s_ids:
        celery_crawl_single_source.delay(s_id)


@shared_task(name="parser.tasks.celery_crawl_all_active_sources_task")
def celery_crawl_all_active_sources_task():
    """
        Задача-роутер для запуска всех активных источников.
        Берет все активные источники из базы и создает для каждого отдельную задачу celery_crawl_single_source.
    """
    active_ids = Source.objects.filter(isActive=True).values_list('id', flat=True)
    for s_id in active_ids:
        celery_crawl_single_source.delay(s_id)
