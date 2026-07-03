# parser/strategies/Strategy.py

import logging

from parser.strategies.registry import PARSER_REGISTRY

logger = logging.getLogger(__name__)


def run(source, headers):
    parser = PARSER_REGISTRY.get(source.sourceType)
    if parser:
        return parser(source, headers)
    else:
        logger.info(f"Not found strategy to parse '{source.sourceType}'")
        return None
