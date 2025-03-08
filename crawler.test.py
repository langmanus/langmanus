from src.crawler.crawler_tool import CrawlerTool

if __name__ == "__main__":
    tool = CrawlerTool()
    print(
        tool.execute(
            "https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
        )
    )
