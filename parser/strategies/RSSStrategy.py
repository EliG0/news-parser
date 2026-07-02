# parser/strategies/RSSStrategy.py

import logging
from typing import List

import feedparser
import requests

from sources.models import Source

logger = logging.getLogger(__name__)


def RSSStrategy(source: Source, headers: dict) -> List[str]:
    logger.info(f"Using RSS strategy to: {source.name} ({source.rss})")
    foundedUrls = set()

    try:
        response = requests.get(source.rss, headers=headers, timeout=10)

        if response.status_code != 200:
            logger.error(f"RSS {source.name} вернул HTTP-код {response.status_code} вместо фида.")
            return []

        feed = feedparser.parse(response.text)

        for post in feed.entries:
            link = post.get("link")
            if link:
                foundedUrls.add(link)

    except Exception as e:
        logger.error(f"Error while parsing RSS from {source.name}: {e}")

    return list(foundedUrls)
