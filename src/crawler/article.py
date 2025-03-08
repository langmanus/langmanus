import re
from urllib.parse import urljoin

from markdownify import markdownify as md


class Article:
    def __init__(self, url: str, title: str, html_content: str):
        self.url = url
        self.title = title
        self.html_content = html_content

    def to_markdown(self, including_title: bool = True) -> str:
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.html_content)
        return markdown

    def to_message_content(self) -> list[dict[str, str]]:
        image_pattern = r"!\[.*?\]\((.*?)\)"

        results: list[dict[str, str]] = []
        parts = re.split(image_pattern, self.to_markdown())

        for i, part in enumerate(parts):
            if i % 2 == 1:
                image_url = urljoin(self.url, part.strip())
                results.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                results.append({"type": "text", "text": part.strip()})

        return results
