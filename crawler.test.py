from src.crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler()
    print(
        crawler.crawl(
            "https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
        ).to_markdown()
    )
