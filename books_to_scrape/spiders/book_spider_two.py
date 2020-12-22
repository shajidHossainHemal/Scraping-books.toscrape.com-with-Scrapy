import scrapy
import os
import urllib.request
from ..items import BooksToScrapeDetailedItem

class BookSecondSpider(scrapy.Spider):
    name = 'book_plus'
    start_urls = [
        'http://books.toscrape.com/'
    ]

    def parse(self, response):
        all_book_list = response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3')

        for book in all_book_list:
            book_url = response.urljoin(book.css('div.image_container a::attr(href)').get())

            yield scrapy.Request(book_url, callback=self.parse_site_contents)
        
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_site_contents(self, response):
        items = BooksToScrapeDetailedItem()

        SITE_URL = self.start_urls[0]

        items['Title'] = response.css('div.col-sm-6.product_main h1::text').get()

        garbage = response.css('p.availability::text').extract()
        items['Availability'] = self.clean_availability(garbage)

        items['Price_excluding_tax'] = response.css('.price_color::text').get()
        items['Price_including_tax'] = response.css('td::text')[3].get()
        items['Tax'] = response.css('td::text')[4].get()
        items['UPC'] = response.css('td::text')[0].get()
        items['Number_of_Reviews'] = response.css('td::text')[6].get()

        image_link = response.css('.active img::attr(src)').get()
        items['Image_Link'] = SITE_URL + self.clean_image(image_link)

        yield items
    
    def clean_image(self, img_link):
        if img_link.find('../') != -1:
            img_link = img_link.replace('../', '')

        return img_link
    
    def clean_availability(self, garbage, str=['', 'In stock']):
        availability = ''
        for element in garbage:
            if element.strip() != str[0] and element.strip() != str[1]:
                availability += element.strip()
        return availability
    
    def download_images(self, url, save_path, file_name):
        # Check if the directory exists, if not make directory
        CHECK_FOLDER = os.path.isdir(save_path)
        if not CHECK_FOLDER:
            os.mkdir(save_path)

        # Download images
        FULL_FILE_NAME = os.path.join(save_path, file_name.split('/')[-1])
        urllib.request.urlretrieve(url, FULL_FILE_NAME)
