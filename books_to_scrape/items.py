# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksToScrapeItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    image = scrapy.Field()

class BooksToScrapeDetailedItem(scrapy.Item):
    Title = scrapy.Field()
    Price_excluding_tax = scrapy.Field()
    Price_including_tax = scrapy.Field()
    Tax = scrapy.Field()
    Availability = scrapy.Field()
    UPC = scrapy.Field()
    Number_of_Reviews = scrapy.Field()
    Image_Link = scrapy.Field()
