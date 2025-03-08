from .jina_client import JinaClient
from .readability_parser import ReadabilityParser


class CrawlerTool:
    name: str = "Crawler"
    description: str = "Crawl the web for information"

    def execute(self, url: str) -> str:
        jina_client = JinaClient()
        parser = ReadabilityParser()
        html = jina_client.crawl_html(url)
        article = parser.parse_article(html)
        return article.content
