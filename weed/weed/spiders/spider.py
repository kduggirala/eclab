import scrapy

class WeedSpider(scrapy.Spider):
    name = "weed"
    page = 1
    def parse(self, response):
        ol = response.xpath("//ol")
        if ol.get():
            for product in ol.xpath("./li/div[2]"):
                first = product.xpath("./div[1]/a/div")
                second = product.xpath("./div[2]/div/div/div/div/div/div/div/div")
                yield {
                    "category" : first.xpath("./div[1]").get(),
                    "name" : first.xpath("./div[2]").get(), 
                    "cbd" : first.xpath("./div[3]").get(),
                    "price" : second.xpath("./div[1]").get(),
                    "weight" : second.xpath("./div[2]").get()
                }
            self.page += 1
            yield response.follow(self.start_urls[0] + f"?page={self.page}")