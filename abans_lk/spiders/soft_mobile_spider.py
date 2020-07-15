import scrapy
from ..SoftItem import SoftItem

class WasiLapSpider(scrapy.Spider):
    name = 'soft_mob'
    start_urls = [
        'https://mysoftlogic.lk/phones-accessories/mobile-phones/c/24'
    ]
 

    def parse(self, response):

        detail_links = response.css('div.product_content > div > div > a.line-clamp.line-clamp-2::attr(href)').getall()

        print(len(detail_links))

        for link in detail_links:
            yield scrapy.Request(
                response.urljoin('https://mysoftlogic.lk'+ link),
                callback=self._parse_nextlink
            )

      

    def _parse_nextlink(self, response):
        product_name = response.css('.product_name::text').get()
        product_price = response.css('#product-promotion-price::text').get().split('\n')[1].strip()
        product_old_price = response.css('#product-price::text').get().split('\n')[1].strip()
        product_image =  response.css('body > div.super_container > div.main-container > div.single_product > div > div > div.col-lg-5.order-lg-2.order-1 > div > img::attr(src)').get() 
        detailed_url = response.request.url


        newProduct = SoftItem()

        newProduct['product_name'] = product_name
        newProduct['product_price'] = product_price
        newProduct['product_old_price'] = product_old_price
        newProduct['product_image'] = product_image
        newProduct['detailed_url'] = detailed_url

        yield newProduct