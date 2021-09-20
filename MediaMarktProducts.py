import json

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class Crawl(scrapy.Spider):
    name="MediaMarkt"
    today = datetime.now().strftime("%Y-%m-%d")
    output = []
    number = 4
    count = 1

    def start_requests(self):
        urls = [
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html",
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view=&page=2",
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view=&page=3",
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view=&page=4",
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view=&page=5",
            "https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html?searchParams=&sort=&view=&page=6"
        ]
        for url in urls:
            req = scrapy.Request(url, callback=self.parse)
            yield req

    def parse(self, response):
        start_name= "\"name\":\""
        end_name = "\",\"id\""

        start_id = "\"id\":\""
        end_id = "\",\"price\""

        start_price = "\"price\":\""
        end_price = "\",\"brand\""

        products=response.css('ul.products-list')
        
        product =  products.css('script').getall()
        for x in range (len(product)):
            if(x%2 == 0):
                name= product[x][product[x].find(start_name)+len(start_name):product[x].rfind(end_name)]
                id= product[x][product[x].find(start_id)+len(start_id):product[x].rfind(end_id)]
                price= product[x][product[x].find(start_price)+len(start_price):product[x].rfind(end_price)]
                self.output.append({
                    "ProductId": id,
                    "ProductName": name,
                    "ProductPrice":price,
                })

                

    def close(self, spider, reason):
        with open(f"{self.name}_{self.today}.json", "w", encoding="utf-8") as f:
            json.dump(self.output, f, ensure_ascii=False)

process = CrawlerProcess()
process.crawl(Crawl)
process.start()