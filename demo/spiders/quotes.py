# -*- coding: utf-8 -*-
from demo.items import Quote
import scrapy
from scrapy import Request
from scrapy.http.response import Response
from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'demo.pipelines.PySolrQuotesPipeline': 1,
            'demo.pipelines.JsonQuotesWriterPipeline': 1
        },
        # 'LOG_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'
        }
    }

    def parse(self, response: Response):
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader(item=Quote(), selector=quote)
            loader.add_css('content', 'span.text')
            loader.add_css('author', 'span small')
            loader.add_css('tags', 'a.tag')
            yield loader.load_item()
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
