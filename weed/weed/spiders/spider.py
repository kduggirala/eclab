import scrapy

class WeedSpider(scrapy.Spider):
    name = "weed"
    custom_settings = { 
        'FEEDS': {f"products_data" + '.jsonl': {'format': 'jsonlines', 'overwrite': False}} 
    }

    def __init__(self, *args, **kwargs):
        self.start_urls = [kwargs.get('start_url')] 
        self.page = 1

    def parse(self, response):
        ol = response.xpath("//ol")
        if ol.get():
            for product in ol.xpath("./li/div[2]"):
                first = product.xpath("./div[1]/a/div")
                second = product.xpath("./div[2]/div/div/div/div/div/div/div/div")
                yield {
                    "category" : first.xpath("./div[1]/text()").get(),
                    "name" : first.xpath("./div[2]/text()").get(), 
                    "cbd" : first.xpath("./div[3]/text()").get(),
                    "price" : second.xpath("./div[1]/text()").get(),
                    "weight" : second.xpath("./div[2]/text()").get(),
                    "url" : self.start_urls[0]
                }
            self.page += 1
            yield response.follow(self.start_urls[0] + f"?page={self.page}")