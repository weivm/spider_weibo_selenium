import time

import scrapy
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from scrapy import Spider
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spider_weibo_selenium.items import SpiderWeiboSeleniumItem


class WbSpider(scrapy.Spider):
    name = "wb"
    allowed_domains = ["weibo.cn"]
    start_urls = ["https://m.weibo.cn/p/106003type=25&t=3&disable_hot=1&filter_type=realtimehot"]

    def __init__(self, *args, **kwargs):
        super(WbSpider, self).__init__(*args, **kwargs)
        self.url = None
        self.count = None
        self.name = None
        self.driver = webdriver.Firefox()

    def parse(self, response, **kwargs):
        self.driver.get(response.url)
        self.driver.implicitly_wait(10)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        element = self.driver.find_element(By.XPATH, "//a[@class='color-gray']")
        element.click()
        self.driver.implicitly_wait(3)

        # 获取所有元素
        elements = self.driver.find_elements(By.XPATH, "//span[@class='main-link m-box m-box-center-a']")

        # 循环遍历所有元素并处理
        for i in range(len(elements)):
            while True:
                try:
                    if i > len(elements) - 1:
                        break
                    time.sleep(2)
                    elements = self.driver.find_elements(By.XPATH, "//span[@class='main-link m-box m-box-center-a']")
                    e = elements[i]
                    print("w_text", e.text)
                    self.name = e.text

                    st = self.driver.find_elements(By.XPATH, "//span[@class='sub-text']")
                    st = st[i]
                    print("w_count", st.text)
                    self.count = st.text

                    e.click()

                    print("w_url", self.driver.current_url)
                    self.url = self.driver.current_url

                    print("Calling getitem...")
                    for item in self.getitem():
                        yield item
                    time.sleep(2)

                    self.driver.execute_script("window.history.go(-1)")
                    break
                except StaleElementReferenceException:
                    print("Element reference is stale. Re-finding elements...")
        pass

    def closed(self, reason):
        self.driver.quit()

    def getitem(self):
        param = SpiderWeiboSeleniumItem()
        param['url'] = self.url
        param['name'] = self.name
        param['count'] = self.count
        yield param
