import scrapy
from ..WasiItem import WasiItem

class WasiLapSpider(scrapy.Spider):
    name = 'wasi_lap'
    start_urls = [
        'https://www.wasi.lk/product-category/electronic-devices/laptops/page/1'
    ]
    page_number = 2

    def parse(self, response):

        detail_links = response.css('.mf-product-details-hover a::attr(href)').getall()
        max_pagenumber = 5

        for link in detail_links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self._parse_nextpage
            )

        next_page = 'https://www.wasi.lk/product-category/electronic-devices/laptops/' + \
                     str(WasiLapSpider.page_number) + ''
        if WasiLapSpider.page_number <= int(max_pagenumber):
            WasiLapSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def _parse_nextpage(self, response):
        product_name = response.css('.entry-title::text').get()
        product_price = response.css('.amount::text').get()
        product_discount = response.css('.onsale::text').get()
        product_image =  response.css('div.mf-product-detail > div.woocommerce-product-gallery.woocommerce-product-gallery--with-images.woocommerce-product-gallery--columns-5.images.without-thumbnails > figure > div > a::attr(href)').get() 


        newProduct = WasiItem()

        newProduct['product_name'] = product_name
        newProduct['product_price'] = product_price
        newProduct['product_discount'] = product_discount
        newProduct['product_image'] = product_image

        yield newProduct