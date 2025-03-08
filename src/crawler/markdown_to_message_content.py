import re
from urllib.parse import urljoin


def markdown_to_message_content(markdown_text, base_url: str):
    # 定义正则表达式来匹配图片 URL
    image_pattern = r"!\[.*?\]\((.*?)\)"

    results: list[dict[str, str]] = []
    parts = re.split(image_pattern, markdown_text)

    for i, part in enumerate(parts):
        if i % 2 == 1:
            url = urljoin(base_url, part.strip())
            results.append({"type": "image_url", "image_url": {"url": url}})
        else:
            results.append({"type": "text", "text": part.strip()})

    return results
