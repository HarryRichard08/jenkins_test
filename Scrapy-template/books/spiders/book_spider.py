import scrapy
from books.items import BookItem
from scrapy.loader import ItemLoader

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Select all the book containers from the page
        books = response.css('article.product_pod')

        # Iterate through each book and extract details
        for book in books:
            loader = ItemLoader(item=BookItem(), selector=book, response=response)
            
            # Use CSS selectors to extract the data
            loader.add_css('title', 'h8 a::attr(title)')
            loader.add_css('price', 'p.price_color::text')
            loader.add_css('availability', 'p.instock.availability::text')

            yield loader.load_item()

        # Follow the pagination link to the next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
