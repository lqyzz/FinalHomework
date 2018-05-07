# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector, Spider
import re
import json
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from scrapy_redis.utils import bytes_to_str

from ..items import SinaNewsItem


class SinaCrawlerSpider(RedisSpider):
    name = 'sina_crawler'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/gov/xlxw/2018-01-29/doc-ifyqzcxh9777323.shtml']

    default_rules = [
        LinkExtractor(allow_domains = allowed_domains, restrict_xpaths=('//a[@href]')),
    ]
        
    
    def make_request_from_data(self, data):
        # 应该只有手动测试的时候要加 replace()
        # 使用json.dumps()输入数据时不用
        json_data = bytes_to_str(data, self.redis_encoding)#.replace("'", "\"")
        json_data = json.loads(json_data, encoding = self.redis_encoding)

        url = json_data['url']
        req = self.make_requests_from_url(url)
        
        if 'priority' in json_data:
            req.priority = int(json_data['priority'])
        if 'rules' in json_data:
            req.meta['rules'] = json_data['rules']

        req.meta['request_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        req.dont_filter = False
            
        return req

    
    def parse(self, response):
        sina_news_item = SinaNewsItem()
        sina_news_item['url'] = response.request.url
        sina_news_item['encoding'] = response.encoding
        sina_news_item['request_time'] = response.request.meta['request_time']
        sina_news_item['html'] = response.text
        sina_news_item['title'] = response.xpath('string(//title)').extract_first()

        yield sina_news_item

        if 'rules' in response.request.meta:
            rules = response.request.meta['rules']
            # rule example: LinkExtractor(allow_domains = allowed_domains, restrict_xpaths=('//a[@href]'))
            
            for rule in rules:
                exec('le = ' + rule)
                links = le.extract_links(response)
                for link in links:
                    req = self.make_requests_from_url(link.url)
                    req.meta['rules'] = rules
                    req.meta['request_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    req.dont_filter = response.request.dont_filter
                    req.priority = response.request.priority
                    yield req
        else:
            for rule in self.default_rules:
                le = rule
                links = le.extract_links(response)
                for link in links:
                    req = self.make_requests_from_url(link.url)
                    req.meta['request_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    req.dont_filter = response.request.dont_filter
                    req.priority = response.request.priority
                    yield req
                



'''
class SinaCrawlerSpider(CrawlSpider):
    name = 'sina_crawler'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/gov/xlxw/2018-01-29/doc-ifyqzcxh9777323.shtml']

    rules = [
        Rule(LinkExtractor(allow_domains = allowed_domains, restrict_xpaths=('//a[@href]')),
             callback = 'sina_parse', follow = False, process_request = 'my_request')
    ]

    def my_request(self, request):
        request.priority = 3
        # True为强制下载相同url的界面
        request.dont_filter = False
        # meta中添加请求时间
        request.meta['request_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return request


    def sina_parse(self, response):
        sina_news_item = SinaNewsItem()
        sina_news_item['url'] = response.request.url
        sina_news_item['encoding'] = response.encoding
        sina_news_item['request_time'] = response.request.meta['request_time']
        sina_news_item['html'] = response.text
        sina_news_item['title'] = response.xpath('string(//title)').extract_first()


        return sina_news_item
'''
