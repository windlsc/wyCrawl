# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TicketSpider(CrawlSpider):
    name = 'ticket'
    allowed_domains = ['money.163.com']
    start_urls = ['http://money.163.com/']
    custom_settings = {
            'ITEM_PIPELINES': {'wyCrawl.pipelines.WycrawlPipeline': 1,
            }
     }

    rules = (
        Rule(LinkExtractor(allow=r'\d{6}\.html#9a01'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['fund_name'] = response.xpath('//div[@class="stock_info"]//td[@class="col_1"]/h1/a/text()').get()
		item['fund_id'] = response.xpath('//div[@class="stock_info"]//td[@class="col_1"]/h1/span/a/text()').get()
        response.xpath('//div[@class="stock_detail"]//tr[@class="stock_bref"]/td[1]/span/text()')
		#item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
