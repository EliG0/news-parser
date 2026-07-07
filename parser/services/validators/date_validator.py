import logging
from datetime import date
from typing import Optional

from parser.config import MAX_ARTICLE_AGE_DAYS

logger = logging.getLogger(__name__)


def is_not_future(dt: date) -> bool:
    return dt <= date.today()


def is_recent(dt: date) -> bool:
    return (date.today() - dt).days <= MAX_ARTICLE_AGE_DAYS


"""
Последовательность функций проверки даты публикации.
Каждая функция должна вернуть True,
если дата считается допустимой.
"""
DATE_VALIDATORS = [
    is_not_future,
    is_recent,
]


def validate_date(parsed_date) -> Optional[date]:
    """
    Проверяет дату публикации, полученную от Trafilatura. Возвращает date или None.
    """

    if not parsed_date:
        return None

    if not all(validator(parsed_date) for validator in DATE_VALIDATORS):
        return None

    return parsed_date
