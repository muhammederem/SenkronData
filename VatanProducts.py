import json

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class Crawl(scrapy.Spider):
    name="Vatan"
    today = datetime.now().strftime("%Y-%m-%d")
    output = []

    def start_requests(self):
        urls = [
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=2",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=3",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=4",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=5",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=6",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=7",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=8",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=9",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=10",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=11",
            "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page=12"
        ]
        for url in urls:
            req = scrapy.Request(url, callback=self.parse)
            yield req

    def parse(self, response):
        products = response.css("div.product-list__content")
        
        product_id  = products.css('div.product-list__product-code::text').getall()
        product_name =  products.css('div.product-list__product-name::text').getall()
        product_price = products.css('span.product-list__price::text').getall()+products.css('span.product-list__decimals::text').getall()
        for x in range (len(product_name)):

            self.output.append({
                "ProductId": product_id[x].replace("\n",""),
                "ProductName": product_name[x].replace("\n",""),
                "ProductPrice":product_price[x],
            })

        # # pagination
        # try:
        #     count = 1
        #     nexturl = "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page="+count
        #     yield scrapy.Request(nexturl, callback=self.parse)
            
        # except:
        #     pass

    def close(self, spider, reason):
        with open(f"{self.name}_{self.today}.json", "w", encoding="utf-8") as f:
            json.dump(self.output, f, ensure_ascii=False)

process = CrawlerProcess()
process.crawl(Crawl)
process.start()