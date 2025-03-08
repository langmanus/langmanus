import os

import requests


class JinaClient:
    def crawl(self, url: str, return_format: str = "html") -> str:
        url = "https://r.jina.ai/https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": return_format,
        }
        if os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            print(
                "WARNING: Jina API key is not set. Provide your own key to access a higher rate limit.",
                "See https://jina.ai/reader for more information.",
            )
        data = {"url": url}
        response = requests.post(url, headers=headers, json=data)
        return response.text
