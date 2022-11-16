import scrapy
from bs4 import BeautifulSoup

class AmzCatSpider(scrapy.Spider):
    name = 'amz_cat'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Best-Sellers-Welcome/zgbs/']

    def parse(self, response):
        soup = BeautifulSoup(response.body,'lxml')
        
        urls = soup.find_all('div',{'role':'treeitem'})
        urls = [x.find('a') for x in urls if "/Best-Sellers" in str(x)]
        
        for x in urls:
            url = "https://www.amazon.com"+x.get('href')
            item = {}
            item['category'] = x.text
            yield item
            yield scrapy.Request(url = url, callback=self.parse_template, meta={'tree': x.text, 'last_i':x.text})
        

    def parse_template(self, response):
        soup = BeautifulSoup(response.body,'lxml')
        last_i = response.meta['last_i']
        sub_cats = soup.find_all('div',{'role':'treeitem'})
        check = False
        for sc in sub_cats:
            if not check:
                if sc.text == last_i:
                    check = True
                continue
            item = {} 
            item['category'] = response.meta['tree'] + ">"+sc.text.strip()
            yield item
            url = "https://www.amazon.com" + sc.find('a').get('href')
            yield scrapy.Request(url = url, callback=self.parse_template, meta={'tree':item['category'], 'last_i':sc.text})
        