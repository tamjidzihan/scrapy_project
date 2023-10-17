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
            print(next_book_url)
            yield response.follow(next_book_url, callback = self.parse_books_url)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_books_url(self,response):
        tables = response.css('table tr')
        yield{
            'name':response.css('.product_main h1::text').get(),
            'product_type': tables[1].css('td::text').get(),
            'price':response.css('p.price_color::text').get(),
            'price_excl_tax':tables[2].css('td::text').get(),
            'price_incl_tax':tables[3].css('td::text').get(),
            'Availability': tables[5].css('td::text').get(),
            'catagory':response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        }