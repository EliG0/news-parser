import logging
from datetime import datetime, date
from typing import *

import trafilatura
from django.utils import timezone
from django.utils.dateparse import parse_date

from parser.services.model import ParsedArticle
from parser.services.validators.date_validator import validate_date

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

                parsed_date = parse_date(published_at)
                validated_date = validate_date(parsed_date)
                published_dt = self._to_datetime(validated_date)

                articles.append(ParsedArticle(
                    url=page["url"],
                    text=text,
                    title=title,
                    published_at=published_dt
                ))
            except Exception:
                logger.exception(f"ExtractService | extract |")

        return articles

    def _to_datetime(self, published_at: date | None) -> datetime | None:
        if published_at is None:
            return None

        naive = datetime.combine(published_at, datetime.min.time())
        return timezone.make_aware(naive)
