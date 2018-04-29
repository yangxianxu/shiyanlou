# -*- coding:utf-8 -*-
import scrapy
class ShiyanlouGithubSpider(scrapy.Spider):

    name = 'shiyanlou-github'
    
    def start_requests(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_tmpl.format(i) for i in range(1,4))
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for course in response.css('div#user-repositories-list ul li'):
            yield {
                #'name':course.css('div h3 a::text').extract_first(),
                'name':course.xpath('.//div/h3/a/text()').re_first('[a-zA-Z0-9\-\_]+'),
                'update_time':course.css('div relative-time::attr(datetime)').extract_first()
                }

