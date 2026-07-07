# parser/strategies/Strategy.py

import logging

from parser.strategies.registry import PARSER_REGISTRY

logger = logging.getLogger(__name__)


def run(source, headers):
    parser = PARSER_REGISTRY.get(source.source_type)
    if parser:
        return parser(source, headers)
    else:
        logger.info(f"Not found strategy to parse '{source.source_type}'")
        return None
