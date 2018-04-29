# -*- coding: utf-8 -*-
import scrapy
from shiyanlou_github.items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,4))

    def parse(self, response):
        for repository in response.css('div ul li'):
            item = RepositoryItem()
            item['name'] = repository.xpath('./div/h3/a/text()').re_first('[a-zA-Z0-9\-\_]+')
            item['update_time'] = repository.css('div relative-time::attr(datetime)').extract_first()
            repository_url = response.urljoin(repository.xpath('./div/h3/a/@href').extract_first())
            print(repository_url)
            print("*"*20)
            request = scrapy.Request(repository_url, callback=self.parse_repository)
            request.meta['item'] = item
            yield request

    def parse_repository(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//div/ul/li[1]/a/span/text()').re_first('[0-9\,]+')
        #item['branches'] = response.xpath('//div[@class="stats-switcher-wrapp    er"]/ul/li[2]/a/span/text()').re_first('[0-9\,]+')
        item['branches'] = response.xpath('//div[@class="stats-switcher-wrapper"]/ul/li[2]/a/span/text()').re_first('[0-9\,]+')
        item['releases'] = response.xpath('//div[@class="stats-switcher-wrapper"]/ul/li[3]/a/span/text()').re_first('[0-9\,]+')
        yield item
