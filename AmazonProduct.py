import json

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class Crawl(scrapy.Spider):
    name="Amazon"
    today = datetime.now().strftime("%Y-%m-%d")
    output = []
    number = 4
    count = 1

    def start_requests(self):
        urls = [
            "https://www.amazon.com.tr/s?k=Cep+Telefonu&i=electronics&rh=n%3A13709907031%2Cp_89%3AApple%7CGENERAL+MOBILE%7COPPO%7COppo+realme%7CSamsung&dc&qid=1630879073&rnid=13493765031&ref=sr_nr_p_89_6",
            "https://www.amazon.com.tr/s?k=Cep+Telefonu&i=electronics&rh=n%3A13709907031%2Cp_89%3AApple%7CGENERAL+MOBILE%7COPPO%7COppo+realme%7CSamsung&dc&page=2&qid=1632082809&rnid=13493765031&ref=sr_pg_2",
            "https://www.amazon.com.tr/s?k=Cep+Telefonu&i=electronics&rh=n%3A13709907031%2Cp_89%3AApple%7CGENERAL+MOBILE%7COPPO%7COppo+realme%7CSamsung&dc&page=3&qid=1632083318&rnid=13493765031&ref=sr_pg_3",
            "https://www.amazon.com.tr/s?k=Cep+Telefonu&i=electronics&rh=n%3A13709907031%2Cp_89%3AApple%7CGENERAL+MOBILE%7COPPO%7COppo+realme%7CSamsung&dc&page=4&qid=1632083342&rnid=13493765031&ref=sr_pg_4"
        ]
        for url in urls:
            req = scrapy.Request(url, callback=self.parse)
            yield req

    def parse(self, response):
        products=response.css('div.s-main-slot.s-result-list.s-search-results.sg-row')
        
        product_name =  products.css('span.a-size-base-plus.a-color-base.a-text-normal::text').getall()
        product_price = products.css('span.a-price-whole::text').getall()
        for x in range (len(product_name)):

            self.output.append({
                # "ProductId": product_id[x].replace("\n",""),
                "ProductName": product_name[x].replace("\n",""),
                "ProductPrice":product_price[x],
            })

        # pagination

        if Crawl.count<4:
            Crawl.count+=1
            nexturl = "hhttps://www.amazon.com.tr/s?k=Cep+Telefonu&i=electronics&rh=n%3A13709907031%2Cp_89%3AApple%7CGENERAL+MOBILE%7COPPO%7COppo+realme%7CSamsung&dc&page="+ str(Crawl.count) +"&qid=1632082781&rnid=13493765031&ref=sr_pg_2"
            yield response.follow(nexturl,callback = self.parse)
                

    def close(self, spider, reason):
        with open(f"{self.name}_{self.today}.json", "w", encoding="utf-8") as f:
            json.dump(self.output, f, ensure_ascii=False)

process = CrawlerProcess()
process.crawl(Crawl)
process.start()