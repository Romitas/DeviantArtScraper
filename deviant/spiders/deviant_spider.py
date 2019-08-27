# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import time
import errno
import os
import scrapy
import pickle
#from selenium import webdriver
from deviant.items import DeviantItem
from deviant.config import *

login = "Aromidas"
password = "cleenock"



class DeviantSpider(scrapy.Spider):
    name = "deviant"

    cookies = {}

    def __init__(self):
#        self.driver = webdriver.Firefox()
        self.start_urls = URLS
        self.total_deviations_scraped = 0

        with open("deviant/cookies.pkl", "rb") as f:
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

    def __exit__(self):
        print("Total deviations scraped: %d" % self.total_deviations_scraped)

    def make_requests_from_url(self, url):
        request = super(DeviantSpider, self).make_requests_from_url(url)
        request.cookies.update(self.cookies)
        return request

    def parse(self, response):
        offset = response.meta.get('offset', 0)

        url = response.url.split('?')[0].strip('/').split('deviantart.com/')[-1].split('/')
        folder_name = '%s_%s' % (url[0], url[-1])
        folder = os.path.join(OUTPUT_FOLDER, folder_name)
        has_deviations_on_the_page = False

        for deviation in response.xpath('//a[contains(@class,"thumb")]/@href'):
            url = deviation.extract()
            print("Found Deviation: " + url)
            has_deviations_on_the_page = True
            self.total_deviations_scraped += 1
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_deviation, meta={'folder': folder})

        if has_deviations_on_the_page:
            offset += 24
            next_page = response.urljoin('?offset=%d' % offset)
            yield scrapy.Request(next_page, cookies=self.cookies, callback=self.parse, meta={'offset': offset})

    def parse_deviation(self, response):
        print ("Parsing deviation:" + response.url)

        folder = response.meta.get('folder', OUTPUT_FOLDER)
        download = response.xpath('//img[@collect_rid]')

        if not download and "Mature Content" in str(response.body):
            print (response.url + ": Mature Content detected, gonna try to bypass")
            download = response.xpath('//img[@collect_rid]')

        if download:
            download = download[-1].xpath('@src')[0].extract()

            extension = download.split('/')[-1].split('?')[0].split('.')[-1]
            author = response.url.split('deviantart.com/')[-1].split('/')[0]
            filename = author + '_' + response.url.split('/')[-1] + '.' + extension

            try:
                os.makedirs(folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            filepath = os.path.join(folder, filename)

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

