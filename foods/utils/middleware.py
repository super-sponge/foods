#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from scrapy.exceptions import IgnoreRequest, NotConfigured
from foods.settings import USER_AGENT_LIST
import random
import urlparse, os, time
import lxml.html.soupparser as soupparser
import lxml.etree as etree


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import THBaseService
from hbase.ttypes import *


from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings


class SavePageToHbaseMiddleware(object):

    def __init__(self, settings):
        self.hbaseThriftHost = settings.get('HBASE_THRIFT_HOST', 'dn1')
        self.hbaseThriftPort = settings.get('HBASE_THRIFT_PORT', '9090')
        self.hbaseTable = settings.get('HBASE_THRIFT_TABLE', 'page')
        self.hbaseTableCf = settings.get('HBASE_THRIFT_CF', 'cf')
        self.hbaseColQualifier = settings.get('HBASE_THRIFT_CFQUALIFIER', 'page')
        trans = TSocket.TSocket(self.hbaseThriftHost, self.hbaseThriftPort)
        self.transport = TTransport.TBufferedTransport(trans)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    """
    提取html中body包含内容，如果内容一致，不更新，否则更新
    """
    def checkAndPut(self, response):

        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        client = THBaseService.Client(protocol)
        self.transport.open()
        rowKey= response.url
        get = TGet(rowKey)
        result = client.get(self.hbaseTable, get)
        update = True
        havePage = False
        for col in result.columnValues:
            if col.family == self.hbaseTableCf and col.qualifier == self.hbaseColQualifier:
                havePage = True
                dom = soupparser.fromstring(col.value)
                colvalue = etree.tostring(dom.xpath("//body")[0])
                dom = soupparser.fromstring(response.body)
                responsevalue = etree.tostring(dom.xpath("//body")[0])

                if colvalue == responsevalue:
                    update = False
                    print "Url not update " + response.url
                else:
                    col.value = response.body
        if update :
            if result.columnValues :
                if havePage:
                    client.put(self.hbaseTable, TPut(rowKey,result.columnValues))
                else:
                    val = TColumnValue(self.hbaseTableCf, self.hbaseColQualifier, response.body)
                    client.put(self.hbaseTable, TPut(rowKey,result.columnValues + [val]))

            else:
                val = TColumnValue(self.hbaseTableCf, self.hbaseColQualifier, response.body)
                client.put(self.hbaseTable, TPut(rowKey,[val]))
        self.transport.close()

        return response

    def process_response(self, request, response, spider):
        return self.checkAndPut(response)

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
