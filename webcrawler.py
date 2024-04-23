import scrapy
from scrapy.exceptions import CloseSpider

class WebCrawler(scrapy.Spider):
    name = 'webcrawler'
    allowed_domains = ['example.com']  # Change to your target domain
    start_urls = ['http://example.com']  # Starting URL

    def __init__(self, domain='', start_url='', max_pages=100, max_depth=3, *args, **kwargs):
        super(WebCrawler, self).__init__(*args, **kwargs)
        if domain:
            self.allowed_domains = [domain]
        if start_url:
            self.start_urls = [start_url]
        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)
        self.pages_crawled = 0

    def parse(self, response):
        if self.pages_crawled >= self.max_pages or response.meta.get('depth', 0) > self.max_depth:
            raise CloseSpider('Reached max pages or depth limit')

        self.pages_crawled += 1
        yield {
            'url': response.url,
            'content': response.text
        }
        links = response.css('a::attr(href)').getall()
        for link in links:
            if self.pages_crawled < self.max_pages:
                yield response.follow(link, self.parse)