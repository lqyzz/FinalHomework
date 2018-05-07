# -*- coding: utf-8 -*-

from scrapy_redis.dupefilter import RFPDupeFilter
import json
import datetime

from .utils import md5

class LXPDupeFilter(RFPDupeFilter):
    
    def request_seen(self, request):
        """Returns True if request was already seen.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        bool False为接受 True为拒绝
        """

        fp = md5(request.url)

        mark = self.server.hget(self.key, fp)
        if mark == None:
            self.server.hset(self.key, fp,\
                         json.dumps({'request_time': request.meta['request_time'],
                                     'hash': 'null'}))
            return False
        
        last_request_time = datetime.datetime.strptime(
            json.loads(mark)['request_time'], '%Y-%m-%d %H:%M:%S')
        this_request_time = datetime.datetime.strptime(
            request.meta['request_time'], '%Y-%m-%d %H:%M:%S')

        difference = this_request_time - last_request_time
        if difference.days < 3:
        #if difference.seconds < 5:
            return True
        
        return False

