# parser/strategies/WebsiteStrategy.py

import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from sources.models import Source

logger = logging.getLogger(__name__)


def WebsiteStrategy(source: Source, headers: dict) -> list[str]:
    logger.info(f"Using Website strategy to: {source}")
    try:
        response = requests.get(source.url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
    except requests.RequestException as e:
        logger.error(f"Ошибка подключения к сайту {source.name}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    foundedLinks = soup.find_all('a', href=True)
    foundedUrls = set()
    for a in foundedLinks:
        href = a.get('href')
        if re.search(source.patterns, href):
            foundedUrls.add(urljoin(source.url, href))

    return list(foundedUrls)
