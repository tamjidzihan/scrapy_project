import scrapy



class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            next_book = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in next_book:
                next_book_url = 'https://books.toscrape.com/' + next_book
            else:
                next_book_url = 'https://books.toscrape.com/catalogue/' + next_book
            yield response.follow(next_book_url, callback = self.parse_books_url)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_books_url(self,response):
        book_detail = response.css