import scrapy
import json
from scrap.items import QuoteItem, AuthorItem

class Spider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    quotes = []
    authors = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author_name = quote.css('small::text').get()
            tags = quote.css('a.tag::text').getall()

            self.quotes.append({
                'text': text,
                'author': author_name,
                'tags': tags
            })

            self.authors.append({'name': author_name})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            with open('quotes.json', 'w') as quotes_file:
                json.dump(self.quotes, quotes_file)

            with open('authors.json', 'w') as authors_file:
                json.dump(self.authors, authors_file)
