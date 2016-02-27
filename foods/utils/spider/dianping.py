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
    shop_telephone1=Field()	# 商家电话1	商家联系电话1
    shop_telephone2=Field()	# 商家电话2	商家联系电话2
    shop_describe=Field()	# 门店介绍	商家门店的具体介绍等信息
    shop_service=Field()	# 门店服务	商家可以提供的WIFI,停车等服务
    speciality=Field()  # 商家特色      商家特色菜品等信息
    shop_hours=Field()	# 营业时间	商家的正常营业时间
    longitude_location=Field()	# 商家经度	商家所属经度
    altitudes_location=Field()	# 商家纬度	商家所属纬度
    shop_type1=Field()	# 商家大类	大类如：美食、酒店、休闲服务等（目前只有美食）
    shop_type2=Field()	# 商家小类	小类如：火锅、川菜、西北菜、小吃等
    district=Field()	# 所属区县	江北区、渝北区、忠县、开县等
    street=Field()	# 所属商圈	大学城、解放碑、观影桥、西城天街等
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
def parse_dianping(response):

    item = DianPingItem()
#定义五个模块变量
    sel3 = response.xpath('//div[@class="breadcrumb"]')
    sel4 = response.xpath('//div[@class="basic-info default nug_shop_ab_pv-a"]')
    sel6 = response.xpath('//div[@class="brief-info"]')
    sel7 = response.xpath('//div[@id="shop-score"]/ul[@class="stars"]')
    sel8 = response.xpath('//div[@class="other J-other"]')
#定义变量数据解析
    shop_name= sel4.xpath('.//h1[@class="shop-name"]/text()').extract_first()
    shop_adress= sel4.xpath('.//span[@itemprop="street-address"]/@title').extract_first()
    shop_telephone1= sel4.xpath('.//p/span[@itemprop="tel"][1]/text()').extract_first()
    shop_telephone2= sel4.xpath('.//p/span[@itemprop="tel"][2]/text()').extract_first()
    shop_describe= sel8.xpath('.//p[3]/text()').extract_first()
    shop_service= ''
    speciality= ''
    shop_hours= sel4.xpath('.//div/p/span[@class="item"]/text()').extract_first()
    lng = re.search(r'lng:([\d]+\.[\d]+)', response.body)
    lat = re.search(r'lat:([\d]+\.[\d]+)', response.body)
    longitude_location= ''
    altitudes_location= ''
    if lng and lat:
        longitude_location= lng.group(1)
        altitudes_location= lat.group(1)


    shop_type1= ''
    shop_type2= sel3.xpath('.//a[4]/text()').extract_first()
    district= sel3.xpath('.//a[2]/text()').extract_first()
    street= sel3.xpath('.//a[3]/text()').extract_first()
    per_consume= sel6.xpath('.//span[@class="item"][2]/text()').extract_first()
    taste_score= sel6.xpath('.//span[@class="item"][3]/text()').extract_first()
    environment_score= sel6.xpath('.//span[@class="item"][4]/text()').extract_first()
    serve_score= sel6.xpath('.//span[@class="item"][5]/text()').extract_first()
    evaluate_number= sel6.xpath('.//span[@class="item"][1]/text()').extract_first()
    shop_photo= ''  # response.xpath('//div[@class="photos"]/a/img/@src').extract_first()
    input_time= time.strftime('')
    update_time= ''
    data_source= ''
#变量数据解析后判断内容是否有空格，若有则替换
    if shop_name:
        shop_name=shop_name.replace('\n','').strip()
    if shop_adress:                         
        shop_adress=shop_adress.replace('\n','').strip()
    if shop_telephone1:                         
        shop_telephone1=shop_telephone1.replace('\n','').strip()
    if shop_telephone2:                         
        shop_telephone2=shop_telephone2.replace('\n','').strip()
    if shop_describe:                         	
        shop_describe=shop_describe.replace('\n','').strip()
    if shop_service:                         
        shop_service=shop_service.replace('\n','').strip()
    if speciality:                         
        speciality=speciality.replace('\n','').strip()
    if shop_hours:                         
        shop_hours=shop_hours.replace('\n','').strip()
    if longitude_location:                         	
        longitude_location=longitude_location.replace('\n','').strip()
    if altitudes_location:                         
        altitudes_location=altitudes_location.replace('\n','').strip()
    if shop_type1:                         
        shop_type1=shop_type1.replace('\n','').strip()
    if shop_type2:                         
        shop_type2=shop_type2.replace('\n','').strip()
    if district:                         
        district=district.replace('\n','').strip()
    if street:                         
        street=street.replace('\n','').strip()
    if per_consume:                         
        per_consume=per_consume.replace('\n','').strip()
    if taste_score:                         
        taste_score=taste_score.replace('\n','').strip()
    if environment_score:                         
        environment_score=environment_score.replace('\n','').strip()
    if serve_score:                         
        serve_score=serve_score.replace('\n','').strip()
    if evaluate_number:                         
        evaluate_number=evaluate_number.replace('\n','').strip()
#    if score5:                         
#        score5=score5.replace('\n','').strip()
#    if score4:                         
#        score4=score4.replace('\n','').strip()
#    if score3:                         
#        score3=score3.replace('\n','').strip()
#    if score2:                         
#        score2=score2.replace('\n','').strip()
#    if score1:                         
#        score1=score1.replace('\n','').strip()
#把最终替换处理后的变量给item
    item['shop_id']= re.search(r'/shop/([\d]+)$', response.url).group(1)
    item['shop_name']= shop_name                              
    item['shop_adress']= shop_adress                   
    item['shop_telephone1']= shop_telephone1               
    item['shop_telephone2']= shop_telephone2               
    item['shop_describe']= shop_describe                 
    item['shop_service']= shop_service                  
    item['speciality']= speciality                    
    item['shop_hours']= shop_hours                    
    item['longitude_location']= longitude_location            
    item['altitudes_location']= altitudes_location            
    item['shop_type1']= shop_type1                    
    item['shop_type2']= shop_type2                    
    item['district']= district                      
    item['street']= street                        
    item['per_consume']= per_consume                   
    item['taste_score']= taste_score                   
    item['environment_score']= environment_score             
    item['serve_score']= serve_score                   
    item['evaluate_number']= evaluate_number
    item['score5']= ''
    item['score4']= ''
    item['score3']= ''
    item['score2']= ''
    item['score1']= '' 
    if sel7:                                          
        score1 = "".join(sel7.xpath('./li[5]/text()').extract())
        score2 = "".join(sel7.xpath('./li[4]/text()').extract())
        score3 = "".join(sel7.xpath('./li[3]/text()').extract())
        score4 = "".join(sel7.xpath('./li[2]/text()').extract())
        score5 = "".join(sel7.xpath('./li[1]/text()').extract())
        
        item['score5']= re.sub(r'[\t\n\s+]', '', score5)
        item['score4']= re.sub(r'[\t\n\s+]', '', score4)
        item['score3']= re.sub(r'[\t\n\s+]', '', score3)
        item['score2']= re.sub(r'[\t\n\s+]', '', score2)
        item['score1']= re.sub(r'[\t\n\s+]', '', score1)       
#    item['score5']= score5                        
#    item['score4']= score4                        
#    item['score3']= score3                        
#    item['score2']= score2                        
#    item['score1']= score1                        
    item['shop_photo']= shop_photo                    
    item['input_time']= input_time                    
    item['update_time']= update_time                   
    item['data_source']= response.url

    return  item


def saveItem(htmlfile, writer):
    html = ''
    with open(htmlfile) as f:
        html = f.read()
    url = 'http://www.dianping.com/shop/' + htmlfile.split('.')[-2]
    response = HtmlResponse(url=url,body=html)
    item = parse_dianping(response)
    if item:
        row = []
        for id in FIELDS_TO_EXPORT_DIANPING:
            row.append(item[id])
        writer.writerow(row)
if __name__ == '__main__':

    outFile = "../hlwdata/data/dianping_new_page.csv"
    infilelst = '../hlwdata/data/url/dianping_page_index.txt'

    csvfile = file(outFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(FIELDS_TO_EXPORT_DIANPING)

    for line in open(infilelst).readlines():
        saveItem(line.rstrip('\n'), writer)

    csvfile.close()