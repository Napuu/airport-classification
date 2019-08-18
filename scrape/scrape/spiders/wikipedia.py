# -*- coding: utf-8 -*-
import scrapy

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['wikipedia.org', 'tools.wmflabs.org']
    start_urls = [
        'https://en.wikipedia.org/w/index.php?search=category%3A+air+bases&limit=500',
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': '1',
        # it's not generally nice to not obey robots.txt but we are going slowly
        # and not opening too many concurrent requests :-)
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DEPTH_LIMIT': 6
    }
    def parse(self, response):
        depth0links = response.xpath('//div[@class="mw-search-result-heading"]')
        for link in depth0links:
            next_page_url = link.xpath('./a/@href').extract_first()
            title = link.xpath('./a/@title').extract_first().lower()
            if ('fields' in title or 'bases' in title or 'installations' in title or 'stations' in title):
                yield scrapy.Request(response.urljoin(next_page_url))
        depth1links = response.xpath('//div[@class="mw-content-ltr"]/ul/li|//div[@class="mw-category-group"]/ul/li')
        for link in depth1links:
            next_page_url = link.xpath('./a/@href').extract_first()
            yield scrapy.Request(response.urljoin(next_page_url))

        depth2links = response.xpath('//span[@class="geo-default"]/parent::a')
        if (not len(depth2links) == 0):
            next_page_url = depth2links[0].xpath('./@href').extract_first()
            if ("type:airport" in next_page_url):
                yield scrapy.Request(response.urljoin(next_page_url))

        depth3targets = response.xpath('//span[@class="geo"]/span/text()').extract()
        if (len(depth3targets) == 2):
            yield {
                'title': response.xpath('//h1[@id="firstHeading"]/text()').extract_first().split(' - ')[1],
                'lat': response.xpath('//span[@class="latitude"]/text()').extract_first(),
                'lng': response.xpath('//span[@class="longitude"]/text()').extract_first(),
            }
