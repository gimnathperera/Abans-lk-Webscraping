# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AbansLkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_model = scrapy.Field()
    product_data = scrapy.Field()
    pass
    pass
