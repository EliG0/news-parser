from parser.strategies.rss_strategy import rss_strategy
from parser.strategies.vk_strategy import vk_strategy
from parser.strategies.website_strategy import website_strategy

PARSER_REGISTRY = {
    "site": website_strategy,
    "rss": rss_strategy,
    "vk": vk_strategy,
}