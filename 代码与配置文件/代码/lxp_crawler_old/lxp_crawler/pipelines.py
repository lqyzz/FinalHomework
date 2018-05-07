# -*- coding: utf-8 -*-

from scrapy_redis.pipelines import RedisPipeline, default_serialize
from scrapy_redis.defaults import SCHEDULER_DUPEFILTER_KEY

import json

from .utils import md5

class LxpCrawlerPipeline(RedisPipeline):
    
    def __init__(self, server,
                 key = SCHEDULER_DUPEFILTER_KEY,
                 serialize_func = default_serialize):
        super().__init__(server, key, serialize_func)
        self.key = SCHEDULER_DUPEFILTER_KEY


    def _process_item(self, item, spider):
        this_hash = md5(item['html'])
        
        key = self.item_key(item, spider)
        fp = md5(item['url'])

        mark = json.loads(self.server.hget(key, fp))
        if mark['hash'] != 'null':
            last_hash = json.loads(mark)['hash']
            if this_hash != last_hash:
                #print('different')
                pass
            else:
                item.is_dup = True
            
            
        self.server.hset(key, fp,\
                         json.dumps({'request_time': item['request_time'],
                                     'hash': md5(item['html'])}))
        
        return item
