import logging

from parser.config import USER_AGENT
from parser.services.download_service import DownloadService
from parser.services.extract_service import ExtractService
from parser.services.match_service import MatchService
from parser.services.pipeline import Pipeline
from parser.services.storage_service import StorageService
from parser.strategies import strategy
from sources.models import Source

logger = logging.getLogger(__name__)


def crawl_single_source(source: Source, keywords: list):
    headers = {
        'User-Agent': USER_AGENT
    }

    logger.info(f"----- Crawling STARTED for source: {source.name} | Keywords: {len(keywords)}")

    links = strategy.run(source, headers)
    if links is None:
        logger.warning(f'No links found for source: {source.name}')
        logger.info(f"----- Crawling FINISHED for source: {source.name} | Result: No links found -----")
        return

    logger.info(f'Founded {len(links)} links')
    pipeline = Pipeline(DownloadService(), ExtractService(), MatchService(keywords), StorageService())
    result = pipeline.run(links, source)

    logger.info(f"----- Crawling FINISHED for source: {source.name} | Result: {result} -----")
