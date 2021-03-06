from scrapy import cmdline
import os,sys


runtype = ''
# runtype = 'meituan'
# runtype = 'dianping'
# runtype = 'nuomi'
# runtype = 'dianpingreview'



if len(sys.argv) >= 2:
    runtype = sys.argv[1]

if runtype == 'meituan':
    os.environ["SCRAPY_SPIDER_NAME"]="MEITUAN"
    cmdline.execute("scrapy crawl meituan -o ../hlwdata/data/meituan_new.csv -t csv -s DEPTH_LIMIT=10".split())
elif runtype == 'dianping':
    os.environ["SCRAPY_SPIDER_NAME"]="DIANPING"
    cmdline.execute("scrapy crawl dianping -o ../hlwdata/data/dianping_new.csv -t csv -s DEPTH_LIMIT=10 -s DOWNLOAD_DELAY=1".split())
elif runtype == 'nuomi':
    os.environ["SCRAPY_SPIDER_NAME"]="NUOMI"
    cmdline.execute("scrapy crawl nuomi -o ../hlwdata/data/nuomi_new.csv -t csv -s DEPTH_LIMIT=3 -s DOWNLOAD_DELAY=1".split())
elif runtype == 'dianpingreview':
    os.environ["SCRAPY_SPIDER_NAME"]="DIANPINGREVIEW"
    cmdline.execute("scrapy crawl dianpingreview -o ../hlwdata/data/dianping_review.csv -t csv -s DEPTH_LIMIT=20 -s DOWNLOAD_DELAY=2".split())

# os.system('./foods/utils/spider/meituan.py')
# os.system('./foods/utils/spider/dianping.py')
# os.system('./foods/utils/spider/nuomi.py')
