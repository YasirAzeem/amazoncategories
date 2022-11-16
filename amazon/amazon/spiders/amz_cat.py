import scrapy


class AmzCatSpider(scrapy.Spider):
    name = 'amz_cat'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    def parse(self, response):
        pass
