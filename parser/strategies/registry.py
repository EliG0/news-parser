# parser/strategies/registry.py

from parser.strategies.RSSStrategy import RSSStrategy
from parser.strategies.VKStrategy import VKStrategy
from parser.strategies.WebsiteStrategy import WebsiteStrategy

PARSER_REGISTRY = {
    "site": WebsiteStrategy,
    "rss": RSSStrategy,
    "vk": VKStrategy,
}