import os

import requests


class JinaClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def crawl_html(self, url: str) -> str:
        url = "https://r.jina.ai/https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": "html",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            print(
                "WARNING: Jina API key is not set. Provide your Jina API key to access a higher rate limit. "
            )
        data = {"url": url}
        response = requests.post(url, headers=headers, json=data)
        return response.text
