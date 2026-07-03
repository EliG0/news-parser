# parser/Crawler.py
import logging

from django.core.cache import cache

from Django.settings import USER_AGENT
from parser.services.DownloadService import DownloadService
from parser.services.ExtractService import ExtractService
from parser.services.MatchService import MatchService
from parser.services.Model import PipelineResult
from parser.services.Pipeline import Pipeline
from parser.services.StorageService import StorageService
from parser.strategies import Strategy
from sources.models import Source, Keyword

logger = logging.getLogger(__name__)


def crawl_single_source(source: Source, keywords: list):
    headers = {
        'User-Agent': USER_AGENT
    }

    logger.info(f"----- Crawling STARTED for source: {source.name} | Keywords: {len(keywords)}")

    pipeline = Pipeline(DownloadService(), ExtractService(), MatchService(keywords), StorageService())

    links = Strategy.run(source, headers)
    logger.info(f'Founded {len(links)} links')
    result = PipelineResult(downloaded=0, extracted=0, matched=0, saved=0)
    if links is not None:
        result = pipeline.run(links, source)

    logger.info(f"----- Crawling FINISHED for source: {source.name} | Result: {result} -----")


def Crawler(sources_queryset=None):
    sources = sources_queryset if sources_queryset is not None else Source.objects.filter(isActive=True)
    keywords = cache.get_or_set(
        'crawler_keywords_list',
        lambda: [k.word.lower() for k in Keyword.objects.all()],
        timeout=600
    )

    if not sources.exists() or len(keywords) == 0:
        logger.info("No active sources or keywords")
        return

    logger.info(f"----- Crawling STARTED | Loaded sources: {sources.count()}, Keywords: {len(keywords)} ------ \n ")

    for source in sources:
        crawl_single_source(source, keywords)

    logger.info("----- Crawling FINISHED -----")
