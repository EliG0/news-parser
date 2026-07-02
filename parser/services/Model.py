# parsers/services/Model.py

from dataclasses import dataclass


@dataclass
class ParsedArticle:
    url: str
    title: str
    text: str
    matchedKeywords: list[str] = None
