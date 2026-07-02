# parser/Crawler.py
import logging

from parser.services.DownloadService import DownloadService
from parser.services.ExtractService import ExtractService
from parser.services.MatchService import MatchService
from parser.services.Pipeline import Pipeline
from parser.services.StorageService import StorageService
from parser.strategies import Strategy
from sources.models import Source, Keyword

logger = logging.getLogger(__name__)


def ParserRun(sources_queryset=None):
    sources = sources_queryset if sources_queryset is not None else Source.objects.filter(isActive=True)
    keywords = [k.word.lower() for k in Keyword.objects.all()]

    if not sources or not keywords:
        logger.info("No data")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    logger.info(f"----- Crawler STARTED ------ \n Loaded sources: {sources.count()}, Keywords: {len(keywords)}")

    pipeline = Pipeline(DownloadService(), ExtractService(), MatchService(keywords), StorageService())

    for source in sources:
        links = Strategy.run(source, headers)
        logger.info(f'Founded {len(links)} links')
        if links:
            pipeline.run(links, source)

    logger.info("----- Crawling FINISHED -----")
