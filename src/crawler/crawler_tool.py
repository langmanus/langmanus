from .jina_client import JinaClient
from .markdown_to_message_content import markdown_to_message_content
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
        markdown = article.to_markdown(including_title=True)
        message_content = markdown_to_message_content(markdown, url)
        return message_content
