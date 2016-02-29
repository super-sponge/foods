#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from scrapy.exceptions import IgnoreRequest, NotConfigured
from foods.settings import USER_AGENT_LIST
import random

import urlparse, os, time

from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings



class SavePageMiddleware(object):
    enabled_setting = 'SAVE_DOWNLOADEDPAGE_ENABLED'

    def __init__(self, settings):
        if not settings.getbool(self.enabled_setting):
            raise NotConfigured

        self.save_path = settings.get('SAVE_DOWNLOADEDPAGE_PATH')
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _save(self, response):
        url = urlparse.urlparse(response.url)
        pagePath = os.path.join(self.save_path, url.hostname)
        if not os.path.exists(pagePath):
            os.mkdir(pagePath)

        pagePath = os.path.join(pagePath, url.path.lstrip('/').replace('/', '.'))
        pageFile = pagePath + '.' + time.strftime('%Y%m%d%H%M%S')
        if response.status == 200:
            with open(pageFile, 'w') as f:
                f.write(response.body)
        with open(os.path.join(self.save_path, 'pageindex.txt'), 'a') as fin:
            fin.write(response.url + ',' + pageFile + ',' + str(response.status) + '\n')

    def process_response(self, request, response, spider):
        self._save(response)
        return response


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class OrderCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        settings = get_project_settings()
        delimiter = settings.get('CSV_DELIMITER', ',')

        kwargs['delimiter'] = delimiter

        fileds = os.environ.get('SCRAPY_SPIDER_NAME', 'DEFAULT')
        fields_to_export = settings.get('FIELDS_TO_EXPORT_' + fileds, [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export

        super(OrderCsvItemExporter, self).__init__(*args, **kwargs)
