from dataclasses import dataclass


@dataclass
class ParsedArticle:
    url: str
    title: str
    text: str
    matched_keywords: list[str] = None
    published_at: str = None


@dataclass
class PipelineResult:
    downloaded: int
    extracted: int
    matched: int
    saved: int

    def __str__(self):
        return f"Downloaded: {self.downloaded}, Extracted: {self.extracted}, Matched: {self.matched}, Saved: {self.saved}"