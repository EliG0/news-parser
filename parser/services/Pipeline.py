# parser/services/Pipeline
import logging
logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, donwloader, extractor, matcher, storage):
        self.downloader = donwloader
        self.extractor = extractor
        self.matcher = matcher
        self.storage = storage

    def run(self, links, source):
        # Ассинхронное скачивание страниц
        pages = self.downloader.download(links)
        logger.info(f"Download {len(pages)} pages")

        # Экстракция статей из страниц
        articles = self.extractor.extract(pages)

        # Поиск ключевых слов
        matched_articles = self.matcher.match(articles)
        logger.info(f"Find {len(matched_articles)} matches")


        # Сохранение статей в БД
        self.storage.save(matched_articles, source)
