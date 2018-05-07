# -*- coding: utf-8 -*-

import scrapy
from scrapy import Item, Field


class BaiduNewsItem(Item):
    url = Field()
    request_time = Field()
    encoding = Field()
    html = Field()
    title = Field()

    is_dup = False
