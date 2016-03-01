#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: liuhb
@license: ***
@contact:
@see: https://github.com/super-sponge

@version: 0.0.1
@todo[0.0.2]: a new module

@note: a comment
@attention: please attention
@bug: a exist bug
@warning: warnings
'''


from scrapy import Item,Field
from scrapy.selector import HtmlXPathSelector
from foods.settings import FIELDS_TO_EXPORT_DIANPING
from scrapy.http import HtmlResponse
import csv,re



import sys,time
reload(sys)
sys.setdefaultencoding('utf8')

class DianPingItem(Item):
    shop_id=Field() # 商家ID	商家代码
    shop_name=Field()   # 商家名称	商家名称
    shop_adress=Field()	# 商家地址	商家具体地址
    shop_telephone=Field()	# 商家电话1	商家联系电话1
    shop_describe=Field()	# 门店介绍	商家门店的具体介绍等信息
    shop_service=Field()	# 门店服务	商家可以提供的WIFI,停车等服务
    speciality=Field()  # 商家特色      商家特色菜品等信息
    shop_hours=Field()	# 营业时间	商家的正常营业时间
    longitude_location=Field()	# 商家经度	商家所属经度
    altitudes_location=Field()	# 商家纬度	商家所属纬度
    nav0 = Field()  #导航栏数据 可以分析出区县与类别
    nav1 = Field()  #导航栏数据 可以分析出区县与类别
    nav2 = Field()
    nav3 = Field()
    nav4 = Field()
    nav5 = Field()
    nav6 = Field()
    nav7 = Field()
    nav8 = Field()
    nav9 = Field()
    per_consume=Field()	# 人均消费	人均消费XX元
    taste_score=Field()	# 口味分	商家口味评分（1-10分）
    environment_score=Field()	# 环境分	商家环境评分（1-10分）
    serve_score=Field()	# 服务分	商家服务评分（1-10分）
    evaluate_number=Field()	# 评价人数	商家累计评价人数
    score5=Field()	# 5分评分个数	评价分为5分的个数
    score4=Field()	# 4分评分个数	评价分为4分的个数
    score3=Field()	# 3分评分个数	评价分为3分的个数
    score2=Field()	# 2分评分个数	评价分为2分的个数
    score1=Field()	# 1分评分个数	评价分为1分的个数
    shop_photo=Field()	# 商家图片	商家门店宣传图片
    input_time=Field()	# 爬取时间	数据首次爬取时间
    update_time=Field()	# 更新时间	数据更新时间--暂可为空
    data_source=Field()	# 数据来源	大众点评

#解析文本内容
def parse_dianping(response, file = None):

    item = DianPingItem()

    item['shop_photo']= ''
    item['update_time']= ''
    item['shop_describe']= ''
    item['shop_service']= ''
    item['speciality']= ''
    if file == None:
        item['input_time']= time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        t = file.split('.')[-1]
        item['input_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(t,"%Y%m%d%H%M%S"))
    item['data_source']= response.url
    item['score5'] = ''
    item['score4'] = ''
    item['score3'] = ''
    item['score2'] = ''
    item['score1'] = ''



    #基本信息
    basic = response.xpath('//div[@id="basic-info"]')

    if not basic:
        return None
    shop_name= basic.xpath('.//h1[@class="shop-name"]/text()').extract_first().replace(u',',' ').replace(u'，',' ')
    quxian = basic.xpath('.//span[@itemprop="locality region"]/text()').extract_first()
    address = basic.xpath('.//span[@itemprop="street-address"]/@title').extract_first().replace(u',',' ').replace(u'，',' ')
    if quxian == None:
        shop_adress = address
    else:
        shop_adress= quxian + '|' + address

    shop_telephone= "|".join(basic.xpath('.//p/span[@itemprop="tel"]/text()').extract())

    item['shop_id']= re.search(r'/shop/([\d]+)$', response.url).group(1)
    item['shop_name'] = shop_name.strip().strip('\n')
    item['shop_adress'] = shop_adress.replace('，','')
    item['shop_telephone'] = shop_telephone

    lng = re.search(r'lng:([\d]+\.[\d]+)', response.body)
    lat = re.search(r'lat:([\d]+\.[\d]+)', response.body)
    longitude_location= ''
    altitudes_location= ''
    if lng and lat:
        longitude_location= lng.group(1)
        altitudes_location= lat.group(1)

    item['longitude_location'] = longitude_location
    item['altitudes_location'] = altitudes_location

    scores = response.xpath('//div[@id="shop-score"]/ul[@class="stars"]')

    if scores:
        score1 = "".join(scores.xpath('./li[5]/text()').extract())
        score2 = "".join(scores.xpath('./li[4]/text()').extract())
        score3 = "".join(scores.xpath('./li[3]/text()').extract())
        score4 = "".join(scores.xpath('./li[2]/text()').extract())
        score5 = "".join(scores.xpath('./li[1]/text()').extract())

        item['score5']= re.sub(r'[\t\n\s+]', '', score5)
        item['score4']= re.sub(r'[\t\n\s+]', '', score4)
        item['score3']= re.sub(r'[\t\n\s+]', '', score3)
        item['score2']= re.sub(r'[\t\n\s+]', '', score2)
        item['score1']= re.sub(r'[\t\n\s+]', '', score1)



    #获取其他内容，包括 别       名  营业时间
    item['shop_hours'] = ''
    other_infos = basic.xpath('.//div[@class="other J-other Hide"]/p[@class="info info-indent"]')
    for other in other_infos:
        info_name = other.xpath('./span[@class="info-name"]/text()').extract_first()
        info_data = other.xpath('./span[@class="item"]/text()').extract_first()
        if info_name == u'营业时间：' and info_data:
            item['shop_hours']= info_data.strip().replace('\n',' ').strip().replace(u',',' ').replace(u'，',' ')
    #获取人均，口味，环境，服务
    item['per_consume'] = '0.0'
    item['taste_score'] = '0.0'
    item['environment_score'] = '0.0'
    item['serve_score'] = '0.0'
    item['evaluate_number'] = '0'

    brief_infos = basic.xpath('.//div[@class="brief-info"]/span/text()').extract()
    for brief in brief_infos:
        lstitem = brief.split(u'：')
        lstlength = len(lstitem)
        idx = brief.find(u'条评论')
        if lstlength == 1 and idx != -1:
            item['evaluate_number'] = brief[0:idx]
        elif lstitem[0] == u'人均':
            item['per_consume'] = lstitem[1].replace('元','')
        elif lstitem[0] == u'口味':
            item['taste_score'] = lstitem[1]
        elif lstitem[0] == u'环境':
            item['environment_score'] = lstitem[1]
        elif lstitem[0] == u'服务':
            item['serve_score'] = lstitem[1]

    #获取导航栏数据用户分析区县，类别
    for i in range(10):
        item['nav' + str(i)] = ''
    nav_infos = response.xpath('//div[@class="breadcrumb"]/a/text()').extract()
    navlength = len(nav_infos)
    for i in range(navlength):
        item['nav' + str(i)] = nav_infos[i].strip().strip('\n').strip()

    return  item


def saveItem(htmlfile, writer):
    html = ''
    with open(htmlfile) as f:
        html = f.read()
    url = 'http://www.dianping.com/shop/' + htmlfile.split('.')[-2]
    response = HtmlResponse(url=url,body=html)
    item = parse_dianping(response, file = htmlfile)
    # t = htmlfile.split('.')[-1]
    # item['input_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(t,"%Y%m%d%H%M%S"))
    if item:
        row = []
        for id in FIELDS_TO_EXPORT_DIANPING:
            row.append(item[id])
        writer.writerow(row)

def parse_all():
    outFile = "../hlwdata/data/dianping_new_page.csv"
    infilelst = '../hlwdata/data/url/dianping_page_index.txt'

    csvfile = file(outFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(FIELDS_TO_EXPORT_DIANPING)

    for line in open(infilelst).readlines():
        saveItem(line.rstrip('\n'), writer)

    csvfile.close()

def parse_one(htmlfile):
    html = ''
    with open(htmlfile) as f:
        html = f.read()
    url = 'http://www.dianping.com/shop/' + htmlfile.split('.')[-2]
    response = HtmlResponse(url=url,body=html)
    item = parse_dianping(response,file=htmlfile)
    if item:
        for id in FIELDS_TO_EXPORT_DIANPING:
            print id+ ': ' + str(item[id])


if __name__ == '__main__':
    parse_all()
    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.36954358.20160229093050')
    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.48130224.20160228131523')
    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.18088299.20160229074648')
    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.10010841.20160229045541')

    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.13919136.20160227224749')
    # parse_one('/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/shop.17198038.20160227225236')
    # parse_one('/home/scrapy/liuhb/hlwdata/data/page/www.dianping.com/shop.10003973.20160227225439')
    # parse_one('/home/scrapy/liuhb/hlwdata/data/page/www.dianping.com/shop.17549115.20160301165701')
