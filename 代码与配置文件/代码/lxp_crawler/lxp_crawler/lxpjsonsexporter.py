# -*- coding: utf-8 -*-

from scrapy.exporters import BaseItemExporter

from scrapy_redis.utils import bytes_to_str
import json

'''
class LXPJsonsExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file

    def finish_exporting(self):
        self.file.close()

    def export_item(self, item):
        self.file.write(bytes(json.dumps(item._values, default = \
                                   lambda obj: obj.__dict__,
                                   sort_keys = True,
                                   indent = 4) + '\n', encoding = item['encoding']))
        self.file.flush()

        

'''
class LXPJsonsExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.filename = file.name

    def finish_exporting(self):
        self.file.close()

    def start_exporting(self):
        self.file = open(self.filename, 'a', errors = 'ignore')

    def export_item(self, item):
        if item.is_dup:
            return

        json_str = json.dumps(item._values, default = \
                              lambda obj: obj.__dict__,
                              sort_keys = True,
                              indent = 4,
                              ensure_ascii = False)
        #print(json_str)
        
        self.file.write(json_str + '\n')
        self.file.flush()

