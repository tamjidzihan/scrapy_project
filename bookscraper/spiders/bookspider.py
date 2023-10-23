import scrapy
from bookscraper.items import BookItem



class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # You can also customise your FEEDS settings here:=>
    # custom_settings = {
    #     'FEEDS' : {
    #         'booksdata.json':{'format':'json'},
    #         'booksdata.csv':{'format':'csv'}
    #           }
    # }

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            next_book = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in next_book:
                next_book_url = 'https://books.toscrape.com/' + next_book
            else:
                next_book_url = 'https://books.toscrape.com/catalogue/' + next_book
            yield response.follow(next_book_url, callback = self.parse_book_url)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_book_url(self,response):
        tables = response.css('table tr')
        bookitem= BookItem()

        bookitem['title']= response.css('.product_main h1::text').get(),
        bookitem['product_type']= tables[1].css('td ::text').get(),
        bookitem['price']= response.css('p.price_color ::text').get(),
        bookitem['price_excl_tax']= tables[2].css('td ::text').get(),
        bookitem['price_incl_tax']= tables[3].css('td ::text').get(),
        bookitem['availability']=  tables[5].css('td ::text').get(),
        bookitem['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        bookitem['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        
        yield bookitem