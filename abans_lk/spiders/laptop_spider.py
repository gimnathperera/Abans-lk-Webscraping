import scrapy
from ..items import AbansLkItem
from scrapy.http import Request

class AbansSpider(scrapy.Spider):
    name="abans_laptop"
    start_urls = [
       'https://buyabans.com/computers?page=1'
    ]
    page_number = 2


    def parse(self, response):
        detail_links = response.css('#filter-container > li > a::attr(href)').getall()
        max_pagenumber = response.css('#columns > div.row > div.sortPagiBar > div > nav > ul > ul > li:nth-child(6) > a ::text').get()
        
        for link in detail_links:
            yield scrapy.Request(
                response.urljoin(link),
                callback = self._parse_nextpage
            )

        next_page = 'https://buyabans.com/computers?page=' + \
            str(AbansSpider.page_number)+''
        if AbansSpider.page_number <= int(max_pagenumber):  
            AbansSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def _parse_nextpage(self, response):
        product_name = response.css('.product-name::text').get()
        product_price = response.css('#item_price::text').get()
        product_model = response.css('.modal-no::text').get()
        product_data = response.css('strong::text').get()
        product_old_price = response.css('#product > div.primary-box.row.all-details > div.pb-right-column.col-xs-12.col-md-5.col-sm-12.detail-con-padding > div.row > div > div.old-price::text').extract()[1].strip('\n')     
        newProduct = AbansLkItem()

        newProduct['product_name'] = product_name
        newProduct['product_price'] = product_price
        newProduct['product_model'] = product_model
        newProduct['product_data'] = product_data
        newProduct['product_old_price'] = product_old_price

        yield newProduct