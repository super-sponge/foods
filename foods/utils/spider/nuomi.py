#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: 刘军强
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
from foods.settings import FIELDS_TO_EXPORT_NUOMI
import csv,re
from scrapy.http import HtmlResponse




import sys,time
reload(sys)
sys.setdefaultencoding('utf8')

class NuomiItem(Item):
    shop_id=Field() # 商家ID	商家代码
    shop_name=Field()   # 商家名称	商家名称
    shop_adress=Field()	# 商家地址	商家具体地址
    shop_telephone1=Field()	# 商家电话1	商家联系电话1
    shop_telephone2=Field()	# 商家电话2	商家联系电话2
    shop_describe=Field()	# 门店介绍	商家门店的具体介绍等信息
    shop_service=Field()	# 门店服务	商家可以提供的WIFI,停车等服务
    shop_hours=Field()	# 营业时间	商家的正常营业时间
    longitude_location=Field()	# 商家经度	商家所属经度
    altitudes_location=Field()	# 商家纬度	商家所属纬度
    shop_type1=Field()	# 商家大类	大类如：美食、酒店、休闲服务等（目前只有美食）
    shop_type2=Field()	# 商家小类	小类如：火锅、川菜、西北菜、小吃等
    shop_shen = Field() #所属于城市
    district=Field()	# 所属区县	江北区、渝北区、忠县、开县等
    street=Field()	# 所属商圈	大学城、解放碑、观影桥、西城天街等
    score=Field()	# 评分	商家的评分（1-5分）
    per_consume=Field()	# 人均消费	人均消费XX元
    evaluate_number=Field()	# 评价人数	商家累计评价人数
    positive_number=Field()	# 好评数	获得好评的个数
    moderate_number=Field()	# 中评数	获得中评的个数
    negative_number=Field()	# 差评数	获得差评的个数
    shop_photo=Field()	# 商家图片	商家门店宣传图片
    input_time=Field()	# 爬取时间	数据首次爬取时间
    update_time=Field()	# 更新时间	数据更新时间--暂可为空
    data_source=Field()	# 数据来源	糯米

#解析文本内容
def parse_nuomi(response, meta = None):

    item = NuomiItem()
#定义两个模块变量
    sel1 = response.xpath('//div[@class="shop-box"]')
    sel2 = response.xpath('//div[@class="level-detail"]')

    item['shop_id']= re.search(r'/shop/([\d]+)$', response.url).group(1)

    shop_name = sel1.xpath('.//h2[@class="shop-title"]/text()').extract_first()
    if  shop_name:
        item['shop_name']= shop_name.replace(u',',' ').replace(u'，',' ')
    else:
        return None
    item['shop_adress']= sel1.xpath('.//p[@class="bd detail-shop-address"]/span/text()').extract_first().replace(u',',' ').replace(u'，',' ')
    item['shop_telephone1']= sel1.xpath('.//p[@class="bd"]/text()').extract_first()
    item['shop_telephone2']= ''
    item['shop_describe']= ''
    item['shop_service']= ''
    item['shop_hours']= ''

    lng = re.search(r"var[\s]+lon[\s]*=[\s]*'([\d]+\.[\d]+)'", response.body)
    lat = re.search(r"var[\s]+lat[\s]*=[\s]*'([\d]+\.[\d]+)'", response.body)
    longitude_location= ''
    altitudes_location= ''
    if lng and lat:
        longitude_location= lng.group(1)
        altitudes_location= lat.group(1)


    item['longitude_location']= longitude_location
    item['altitudes_location']= altitudes_location
    item['shop_type1']= ''
    item['shop_type2']= ''
    item['shop_shen']= ''
    item['district']= ''
    if meta:
        if meta.has_key('shopCityName'):
            item['shop_shen']= meta['shopCityName']
        if meta.has_key('district'):
            item['district']= meta['district']
    item['street']= ''
    item['score']= sel1.xpath('.//p/span[@class="score"]/text()').extract_first()
    item['per_consume']= sel1.xpath('.//p/span/strong/text()').extract_first()
    item['evaluate_number']= sel1.xpath('.//p/span/a/text()').extract_first()
    item['positive_number']= sel2.xpath('.//div/span[@class="levels qa-hook-good-num"]/text()').extract_first()
    item['moderate_number']= sel2.xpath('.//div/span[@class="levels qa-hook-normal-num"]/text()').extract_first()
    item['negative_number']= sel2.xpath('.//div/span[@class="levels qa-hook-bad-num"]/text()').extract_first()
    # item['shop_photo']= sel1.xpath('.//div[@class="shop-logo"]/img/@src').extract_first()
    item['shop_photo']= ''
    item['input_time']= time.strftime('')
    item['update_time']= ''
    item['data_source']= response.url

    return  item

def saveItem(htmlfile, writer):
    html = ''
    with open(htmlfile) as f:
        html = f.read()
    url = 'http://www.nuomi.com/shop/' + htmlfile.split('.')[-2]
    response = HtmlResponse(url=url,body=html)
    item = parse_nuomi(response)
    # t = htmlfile.split('.')[-1]
    # item['input_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(t,"%Y%m%d%H%M%S"))
    if item:
        row = []
        for id in FIELDS_TO_EXPORT_NUOMI:
            row.append(item[id])
        writer.writerow(row)

if __name__ == '__main__':
    outFile = "../hlwdata/data/nuomi_new_page.csv"
    infilelst = '../hlwdata/data/url/nuomi_page_index.txt'
    # outFile = "/home/sponge/scrapy/hlwdata/data/nuomi_new_page.csv"
    # infilelst = '/home/sponge/scrapy/hlwdata/data/url/nuomi_page_index.txt'


    csvfile = file(outFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(FIELDS_TO_EXPORT_NUOMI)

    for line in open(infilelst).readlines():
        print line
        saveItem(line.rstrip('\n'), writer)

    csvfile.close()
