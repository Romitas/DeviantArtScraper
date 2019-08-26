# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import time
import errno
import os
import scrapy
import pickle
from selenium import webdriver
from deviant.items import DeviantItem
from deviant.config import *

login = "Aromidas"
password = "cleenock"


class DeviantSpider(scrapy.Spider):
    name = "deviant"

    cookies = {}

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.start_urls = URLS

        with open("cookies.pkl", "rb") as f:
            cookies_data = pickle.load(f)
            for i in cookies_data:
                self.cookies[i['name']] = i['value']
            print("Cookies loaded sucessfully: ")
            print(self.cookies)

        self.allowed_domains = []
        for i in self.start_urls:
            domain = i.replace('http://', '')
            domain = i.replace('https://', '')
            domain = domain.split('/')[0]
            self.allowed_domains.append(domain)

        self.folder = self.allowed_domains[0].split('.')[0]

    def __exit__(self):
        self.driver.close()


    def make_requests_from_url(self, url):
        request = super(DeviantSpider, self).make_requests_from_url(url)
        request.cookies.update(self.cookies)
        return request


    def parse(self, response):
        for deviation in response.xpath('//a[contains(@class,"thumb")]/@href'):
            url = deviation.extract()
            print("Found Deviation: " + url)
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_deviation)

        pagination = response.xpath('//div[@class="pagination"]/ul[@class="pages"]/li[@class="next"]')
        if pagination:
            pagination = pagination[0]
        next_page = pagination.xpath('a[not (contains (@class, "disabled"))]/@href').extract()

        if next_page:
            next_page = next_page[0].split('/')[-1]
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_deviation(self, response):
        print ("Parsing deviation:" + response.url)
        download = response.xpath('//img[@collect_rid]')

        if not download and "Mature Content" in response.body:
            #TODO: Use selenium once and to throw cookies to Scrapy, so that it can continue all by itself
            print (response.url + ": Mature Content detected, gonna try to bypass")
            self.driver.get(response.url)

            try:
                month = self.driver.find_element_by_xpath('//input[@id="month"]')
                day   = self.driver.find_element_by_xpath('//input[@id="day"]')
                year  = self.driver.find_element_by_xpath('//input[@id="year"]')
    
                agree   = self.driver.find_element_by_xpath('//input[@id="agree_tos"]')
                submit  = self.driver.find_element_by_xpath('//input[contains(@class, "submitbutton")]')
    
                month.send_keys('10')
                day.send_keys('21')
                year.send_keys('1990')
    
                agree.click()
                submit.click()
            except:
                pass

            sel = scrapy.Selector(text=self.driver.page_source)
            download = sel.xpath('//img[@collect_rid]')


        if download:
            download = download[-1].xpath('@src')[0].extract()

            extension = download.split('/')[-1].split('?')[0].split('.')[-1]
            filename = response.url.split('/')[-1] + '.' + extension

            try:
                os.makedirs(self.folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            filepath = self.folder + '/' + filename

            if not os.path.isfile(filepath):
                print (filename + ": don't have this one, gonna download")
                urlretrieve(download, filepath)
            else:
                print (filename + ": I already have it, skipping")

#            about = response.xpath('//div[@class="dev-view-about-content"]')
#            item = DeviantItem()
#            item['name'] = about.xpath('div[@class="dev-title-container"]/h1/a/@text').extract()
#            item['author'] = about.xpath('div[@class="dev-title-container"]/h1/small/span[@class="username-with-symbol u"]/a[@class="u regular username"/@text').extract()
#            item['url'] = download
#
#            yield item

