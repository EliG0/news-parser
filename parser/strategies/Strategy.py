# parser/strategies/Strategy.py

import logging

from parser.strategies.RSSStrategy import RSSStrategy
from parser.strategies.VKStrategy import VKStrategy
from parser.strategies.WebsiteStrategy import WebsiteStrategy


logger = logging.getLogger(__name__)

PARSER_REGISTRY = {
    "site": WebsiteStrategy,
    "rss": RSSStrategy,
    "vk": VKStrategy,
}

def run(source, headers):
    parser = PARSER_REGISTRY.get(source.sourceType)
    if parser:
        return parser(source, headers)
    else:
        logger.info(f"Not found strategy to parse '{source.sourceType}'")
        return None
