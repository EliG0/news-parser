# parser/services/ExtractService.py
from typing import *

import trafilatura

from parser.services.Model import ParsedArticle


class ExtractService:

    def extract(self, downloaded: List[Dict]) -> List[ParsedArticle]:

        articles = []

        for page in downloaded:
            extract = trafilatura.bare_extraction(
                page['html'],
                with_metadata=True,
            )

            if not extract:
                continue

            if isinstance(extract, dict):
                title = extract.get("title") or "Без заголовка"
                text = extract.get("text") or ""
            else:
                title = getattr(extract, "title", "Без заголовка")
                text = getattr(extract, "text", "")

            articles.append(ParsedArticle(
                url=page["url"],
                text=text,
                title=title
            ))

        return articles