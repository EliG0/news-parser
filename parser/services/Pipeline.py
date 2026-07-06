# parser/services/Pipeline
import logging

from parser.services.Model import PipelineResult

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, downloader, extractor, matcher, storage):
        self.downloader = downloader
        self.extractor = extractor
        self.matcher = matcher
        self.storage = storage

    def run(self, links, source) -> PipelineResult:
        # Ассинхронное скачивание страниц
        downloaded_pages = self.downloader.download(links)
        logger.info(f"Download {len(downloaded_pages)} pages")

        # Экстракция статей из страниц
        extracted_articles = self.extractor.extract(downloaded_pages)

        # Поиск ключевых слов
        matched_articles = self.matcher.match(extracted_articles)
        logger.info(f"Find {len(matched_articles)} matches")

        # Сохранение статей в БД
        saved_articles_count = self.storage.save(matched_articles, source)
        logger.info(f"Save {saved_articles_count} articles")

        return PipelineResult(
            downloaded=len(downloaded_pages),
            extracted=len(extracted_articles),
            matched=len(matched_articles),
            saved=saved_articles_count
        )