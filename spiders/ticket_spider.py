# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from wyCrawl.items import WycrawlItem


class TicketSpider(CrawlSpider):
    name = 'ticket'
    allowed_domains = ['money.163.com']
    start_urls = ['http://money.163.com/']
    #start_urls = ['http://quotes.money.163.com/0601857.html#3a01']
    custom_settings = {
            'ITEM_PIPELINES': {'wyCrawl.pipelines.WycrawlPipeline': 1,
            }
     }

    rules = (
        #Rule(LinkExtractor(allow=r'\/\d{6}\.html'), callback='parse_item', follow=True, process_request='build_request' ),
        Rule(LinkExtractor(allow=r'.*quotes.*\/\d{6}\.html'), callback='parse_item', follow=True, ),
    )

    def start_requests(self):
        for url in self.start_urls:
            print("进入首页")
            print(url)
            yield scrapy.Request(url)
            
    def parse_item(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        item = WycrawlItem()
        item['ticket_name'] = response.xpath('//div[@class="stock_info"]//td[@class="col_1"]/h1/a/text()').get()
        item['ticket_id'] = response.xpath('//div[@class="stock_info"]//td[@class="col_1"]/h1/span/a/text()').get()
        #item['ticket_date'] = response.xpath('//div[@class="stock_detail"]//tr[@class="stock_bref"]/td[1]/span/text()').get()
        #item['ticket_price'] = response.xpath('//div[@class="stock_detail"]//td[@class="price"]/span/text()').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item

    def build_request(self, rule, link):
        print("abc")
        # print(link.url)
        # print(link.text)
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5}, meta={'real_url': request.url})
        r.meta.update(rule=rule, link_text=link.text)
        return r
        
    #def _requests_to_follow(self, response):
    #    if not isinstance(response, HtmlResponse):
    #        return
    #    from scrapy.shell import inspect_response
    #    #inspect_response(response, self)
    #    seen = set()
    #    
    #    #newresponse = response.replace(url=response.meta.get('real_url'))
    #    for n, rule in enumerate(self._rules):
    #        links = [lnk for lnk in rule.link_extractor.extract_links(response)
    #                 if lnk not in seen]
    #        print(links)
    #        print(type(rule))
    #        if links and rule.process_links:
    #            links = rule.process_links(links)
    #        print("奈斯")
    #        print(len(links))
    #        for link in links:
    #            # print(link)
    #            seen.add(link)
    #            # print("啊哈")
    #            r = self._build_request(n, link)
    #            yield rule.process_request(r)