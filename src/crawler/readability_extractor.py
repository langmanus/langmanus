from readabilipy import simple_json_from_html_string

from .article import Article


class ReadabilityExtractor:
    def extract_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            content=article.get("content"),
            url=article.get("url"),
        )
