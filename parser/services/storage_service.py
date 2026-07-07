import logging

from parser.models import Article
from django.db import transaction

logger = logging.getLogger(__name__)


class StorageService:
    def save(self, articles, source):
        count = 0
        with transaction.atomic():
            for article in articles:
                db_article, created = Article.objects.update_or_create(
                    url=article.url,
                    defaults={
                        "source": source,
                        "title": article.title,
                        "text": article.text,
                        "words": ", ".join(article.matchedKeywords),
                    }
                )
                if created:
                    logger.info(f"[+]: {db_article.title}")
                    count += 1
        return count
