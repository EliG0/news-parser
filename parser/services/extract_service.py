import logging
from typing import *

import trafilatura

from parser.services.model import ParsedArticle

logger = logging.getLogger(__name__)


class ExtractService:

    def extract(self, downloaded: List[Dict]) -> List[ParsedArticle]:

        articles = []

        for page in downloaded:
            try:
                extract = trafilatura.bare_extraction(
                    page['html'],
                    with_metadata=True,
                )

                if not extract:
                    continue

                if isinstance(extract, dict):
                    title = extract.get("title") or "Без заголовка"
                    text = extract.get("text") or ""
                    published_at = extract.get("date")
                else:
                    title = getattr(extract, "title", "Без заголовка")
                    text = getattr(extract, "text", "")
                    published_at = getattr(extract, "date", None)

                articles.append(ParsedArticle(
                    url=page["url"],
                    text=text,
                    title=title,
                    published_at=published_at
                ))
            except Exception as e:
                logger.info(f"ExtractService | extract | Error: {e}")

        return articles
