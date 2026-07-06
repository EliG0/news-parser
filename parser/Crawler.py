# parser/Crawler.py
import logging

from parser.config import USER_AGENT
from parser.services.DownloadService import DownloadService
from parser.services.ExtractService import ExtractService
from parser.services.MatchService import MatchService
from parser.services.Pipeline import Pipeline
from parser.services.StorageService import StorageService
from parser.strategies import Strategy
from sources.models import Source

logger = logging.getLogger(__name__)


def crawl_single_source(source: Source, keywords: list):
    headers = {
        'User-Agent': USER_AGENT
    }

    logger.info(f"----- Crawling STARTED for source: {source.name} | Keywords: {len(keywords)}")

    links = Strategy.run(source, headers)
    if links is None:
        logger.warning(f'No links found for source: {source.name}')
        logger.info(f"----- Crawling FINISHED for source: {source.name} | Result: No links found -----")
        return

    logger.info(f'Founded {len(links)} links')
    pipeline = Pipeline(DownloadService(), ExtractService(), MatchService(keywords), StorageService())
    result = pipeline.run(links, source)

    logger.info(f"----- Crawling FINISHED for source: {source.name} | Result: {result} -----")
