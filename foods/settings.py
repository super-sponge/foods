# -*- coding: utf-8 -*-

# Scrapy settings for foods project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'foods'

SPIDER_MODULES = ['foods.spiders']
NEWSPIDER_MODULE = 'foods.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 4

COOKIES_ENABLED = True
# COOKIES_DEBUG = True
# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36'
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html

DEPTH_LIMIT = 5
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

DOWNLOADER_MIDDLEWARES = {
    'foods.utils.middleware.RandomUserAgentMiddleware':400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'foods.utils.middleware.CustRedirectMiddleware':543,
    'foods.utils.middleware.SavePageMiddleware':545
}
REDIRECT_ENABLED=False
REDIRECT_SAVE_ENABLED = True

#保存处理失败的代码
REDIRECT_ERROR_PATH='../hlwdata/data/start_url.txt'
#保存处理过的代码
REDIRECT_DOWNLOADED_PATH='../hlwdata/data/downloaded_url.txt'
#保存网页
SAVE_DOWNLOADEDPAGE_ENABLED=True
SAVE_DOWNLOADEDPAGE_PATH='../hlwdata/data/page'

USER_AGENT_LIST = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'foods.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


FIELDS_TO_EXPORT_MEITUAN = ['shop_id','shop_name','shop_adress','shop_telephone1','shop_telephone2','shop_describe','shop_service','speciality','shop_hours','longitude_location','altitudes_location','shop_type1','shop_type2','district','street','score','consume_number','evaluate_number','shop_photo','input_time','update_time','data_source']
FIELDS_TO_EXPORT_NUOMI = ['shop_id','shop_name','shop_adress','shop_telephone1','shop_telephone2','shop_describe','shop_service','shop_hours','longitude_location','altitudes_location','shop_type1','shop_type2','shop_shen','district','street','score','per_consume','evaluate_number','positive_number','moderate_number','negative_number','shop_photo','input_time','update_time','data_source']
FIELDS_TO_EXPORT_DIANPING = [ 'shop_id','shop_name','shop_adress','shop_telephone','shop_describe','shop_service','speciality','shop_hours','longitude_location','altitudes_location','nav0','nav1','nav2','nav3','nav4','nav5','nav6','nav7','nav8','nav9','per_consume','taste_score','environment_score','serve_score','evaluate_number','score5','score4','score3','score2','score1','shop_photo','input_time','update_time','data_source']

CSV_DELIMITER = ','
FEED_EXPORTERS = {
    'csv': 'foods.utils.middleware.OrderCsvItemExporter',
}
# FEED_URI = u'file:///home/sponge/scrapy/foods/data/product_data.csv'
# FEED_URI = u'file:///home/sponge/scrapy/foods/data/product_data.csv'
# FEED_FORMAT = 'CSV'

# FEED_URI = u'file:///home/sponge/scrapy/foods/data/shop_nuomi.csv'
# FEED_FORMAT = 'CSV'

# FEED_URI = u'file:///home/sponge/scrapy/foods/data/shopindex.csv'
# FEED_FORMAT = 'CSV'

