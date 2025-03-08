from .jina_client import JinaClient
from .readability_extractor import ReadabilityExtractor


class CrawlerTool:
    name: str = "Crawler"
    description: str = "Crawl the web for information"

    def execute(self, url: str) -> list[dict[str, str]]:
        # To help LLMs better understand content, we extract clean
        # articles from HTML, convert them to markdown, and split
        # them into text and image blocks for one single and unified
        # LLM message.
        #
        # Jina is not the best crawler on readability, however it's
        # much easier and free to use.
        #
        # Instead of using Jina's own markdown converter, we'll use
        # our own solution to get better readability results.
        jina_client = JinaClient()
        html = jina_client.crawl_html(url)
        extractor = ReadabilityExtractor()
        article = extractor.extract_article(html)
        message_content = article.to_message_content()
        return message_content
