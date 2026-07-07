import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from sources.models import Source

logger = logging.getLogger(__name__)


def website_strategy(source: Source, headers: dict) -> list[str]:
    logger.info(f"Using Website strategy to: {source}")
    try:
        response = requests.get(source.url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
    except requests.RequestException as e:
        logger.error(f"Ошибка подключения к сайту {source.name}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    founded_links = soup.find_all('a', href=True)
    founded_urls = set()
    for a in founded_links:
        href = a.get('href')
        if re.search(source.patterns, href):
            founded_urls.add(urljoin(source.url, href))

    return list(founded_urls)
