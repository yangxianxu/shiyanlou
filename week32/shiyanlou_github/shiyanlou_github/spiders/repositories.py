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
            item = RepositoryItem({
                'name':repository.xpath('./div/h3/a/text()').re_first('[a-zA-Z0-9\-\_]+'),
                'update_time':repository.css('div relative-time::attr(datetime)').extract_first()
                })
            yield item
