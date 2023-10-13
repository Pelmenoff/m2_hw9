from scrap.spiders.spider import Spider
from scrap.items import QuoteItem, AuthorItem
from scrap.database import db, Author, Quote
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import JsonItemExporter
import json

process = CrawlerProcess({
    'FEED_FORMAT': 'jsonlines',
    'FEED_URI': 'quotes.json'
})
process.crawl(Spider)
process.start()

with open('quotes.json', 'r') as quotes_file:
    quotes_data = json.load(quotes_file)

with open('authors.json', 'r') as authors_file:
    authors_data = json.load(authors_file)

db.connect()

for author_data in authors_data:
    author, created = Author.get_or_create(name=author_data['name'])

for quote_data in quotes_data:
    author = Author.get(Author.name == quote_data['author'])
    Quote.create(text=quote_data['text'], author=author)

db.close()
