# -*- coding: utf-8 -*-

import urllib
import errno
import os
import scrapy
from deviant.items import DeviantItem

class DeviantSpider(scrapy.Spider):
    name = "deviant"

    allowed_domains = ["blackassassin999.deviantart.com"]
    start_urls = [
#            "http://viaestelar.deviantart.com/gallery/"
            "http://blackassassin999.deviantart.com/gallery/51077384/other-fan-art"
            ]
    folder = allowed_domains[0].split('.')[0]

#    def parse(self, response):
#        yield parse_page_follow_next(response)

    def parse(self, response):
        for deviation in response.xpath('//a[@class="thumb"]/@href'):
            url = deviation.extract()
            print url
            yield scrapy.Request(url, callback=self.parse_deviation)

        pagination = response.xpath('//div[@class="pagination"]/ul[@class="pages"]/li[@class="next"]')[0]
        next_page = pagination.xpath('a[not (contains (@class, "disabled"))]/@href').extract()
        if next_page:
            next_page = next_page[0].split('/')[-1]
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_deviation(self, response):
#        download = response.xpath('//div[@class="dev-meta-actions"]/a[@class="dev-page-button dev-page-button-with-text dev-page-download"]/@href')[0].extract()

#        if not download:
#        download = response.xpath('//img[@class="dev-content-normal "]/@src')[0].extract()
        download = response.xpath('//img[@collect_rid]')[-1].xpath('@src')[0].extract()
#        download = response.xpath('//img')[-1]
#        download = download.xpath('@src')[0].extract()
        print download


        if download:
            filename = download.split('/')[-1]

            try:
                os.makedirs(self.folder)
            except OSError, exc:
                if exc.errno != errno.EEXIST:
                    raise

#            call(["mkdir " + self.folder])
            filepath = self.folder + '/' + filename
#            filepath = filename
            urllib.urlretrieve(download, filepath)

#            about = response.xpath('//div[@class="dev-view-about-content"]')
#            item = DeviantItem()
#            item['name'] = about.xpath('div[@class="dev-title-container"]/h1/a/@text').extract()
#            item['author'] = about.xpath('div[@class="dev-title-container"]/h1/small/span[@class="username-with-symbol u"]/a[@class="u regular username"/@text').extract()
#            item['url'] = download
#
#            yield item

