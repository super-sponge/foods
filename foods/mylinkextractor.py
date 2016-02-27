"""
Link extractor based on LxmlLinkExtractor
"""

from scrapy.linkextractors import  LinkExtractor


class MyLinkExtractor(LinkExtractor):
    def __init__(self, allow=(), download = []):
        super(MyLinkExtractor, self).__init__(allow=allow)
        self.downloaded = download

    def extract_links(self, response):
        result = []
        for link in super(MyLinkExtractor, self).extract_links(response):
            if link.url not in self.downloaded:
                result.append(link)
            else:
                print "Exists  %s" % link.url
        return result