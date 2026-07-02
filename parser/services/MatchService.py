# parser/services/MatchService.py
import re


class MatchService:
    def __init__(self, keywords):
        escaped = map(re.escape, keywords)

        regex = r"\b(?:%s)\b" % "|".join(escaped)

        self.pattern = re.compile(
            regex,
            re.IGNORECASE
        )

    def match(self, articles):
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
