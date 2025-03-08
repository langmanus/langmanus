from markdownify import markdownify as md


class Article:
    def __init__(self, title: str, content: str, url: str):
        self.title = title
        self.content = content
        self.url = url

    def to_markdown(self, including_title: bool = True) -> str:
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.content)
        return markdown
