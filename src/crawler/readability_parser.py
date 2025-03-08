from readabilipy import simple_json_from_html_string


class Article:
    def __init__(self, title: str, content: str, url: str):
        self.title = title
        self.content = content
        self.url = url


class ReadabilityParser:
    def parse_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            content=article.get("content"),
            url=article.get("url"),
        )
