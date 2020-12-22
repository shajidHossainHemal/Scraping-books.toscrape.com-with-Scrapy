# First Spider
import scrapy
from ..items import BooksToScrapeItem
import urllib.request
import os

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        'http://books.toscrape.com/'
    ]

    def parse(self, response):
        items = BooksToScrapeItem()

        all_books_list = response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3')

        for book in all_books_list:
            title = book.css('article.product_pod h3 a::attr(title)').extract()
            price = book.css('p.price_color::text').extract()
            garbage_stock = book.css('p.instock::text').extract()
            image = book.css('div.image_container img::attr(src)').extract()
            image = self.clean_image(image)
            stock = self.clean_stock(garbage_stock)

            # Download the images
            SITE_URL = 'http://books.toscrape.com/'
            FILE_NAME = image[0]
            DOWNLOAD_URL = SITE_URL + FILE_NAME
            SAVE_PATH = r'C:\Users\USER\Desktop\Scrapy Projects\books_to_scrape\images'

            # self.download_images(DOWNLOAD_URL, SAVE_PATH, FILE_NAME)
            
            items['image'] = image
            items['stock'] = stock
            items['price'] = price
            items['title'] = title

            yield items
        
        # Load next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def download_images(self, url, save_path, file_name):
        # Check if the directory exists, if not make directory
        CHECK_FOLDER = os.path.isdir(save_path)
        if not CHECK_FOLDER:
            os.mkdir(save_path)
        
        # Download images
        FULL_FILE_NAME = os.path.join(save_path, file_name.split('/')[-1])
        urllib.request.urlretrieve(url, FULL_FILE_NAME)
    
    def clean_stock(self, garbage, str=''):
        stock = []
        for element in garbage:
            if element.strip() != str:
                stock.append(element.strip())
        return stock

    def clean_image(self, img_list):
        if img_list[0].find('../') != -1:
            img_list[0] = img_list[0].replace('../', '')
        
        return img_list

