from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
 
class SeleniumMiddleware():
   def __init__(self, timeout=None, service_args=[]):
       self.logger = getLogger(__name__)
       self.timeout = timeout
       #self.browser = webdriver.PhantomJS(service_args=service_args)
       self.browser = webdriver.Firefox()
       self.browser.set_window_size(1400, 700)
       self.browser.set_page_load_timeout(self.timeout)
       self.wait = WebDriverWait(self.browser, self.timeout)
 
   def __del__(self):
       self.browser.close()
 
   def process_request(self, request, spider):
       """
       用PhantomJS抓取页面
       :param request: Request对象
       :param spider: Spider对象
       :return: HtmlResponse
       """
       self.logger.debug('PhantomJS is Starting')
       try:
           self.browser.get(request.url)
           self.wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="stock_detail"]//tr[@class="stock_bref"]/td[1]/span/text()'), str(page)))
           return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
       except TimeoutException:
           return HtmlResponse(url=request.url, status=500, request=request)
 
   @classmethod
   def from_crawler(cls, crawler):
       return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                  service_args=crawler.settings.get('FIREFOX_SERVICE_ARGS'))