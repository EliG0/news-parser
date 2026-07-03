# parser/services/MatchService.py
import re

from parser.services.Model import ParsedArticle


class MatchService:
    def __init__(self, keywords):
        escaped = map(re.escape, keywords)

        regex = r"\b(?:%s)\b" % "|".join(escaped)

        self.pattern = re.compile(
            regex,
            re.IGNORECASE
        )

    def match(self, articles: list[ParsedArticle]) -> list[ParsedArticle]:
        result = []
        for article in articles:
            title = (article.title or "").lower()
            text = (article.text or "").lower()
            combined = f"{title} {text}"

            matchedWords = sorted(list(set(self.pattern.findall(combined))))

            if matchedWords:
                article.matchedKeywords = matchedWords
                result.append(article)

        return result
