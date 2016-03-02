# 数据爬取启动网址
## 爬取启动配置文件
### 美团
    meituan_start_url.txt
    select distinct data_source from mid_shop_mt_info 
### 糯米
    nuomi_deal_start_url.txt
    
### 点评
    dianping_start_url.txt
    
## 爬去注意事项
* 糯米网容易链接进其他省市的地址，故在每次爬取后需要把其他省市的地址提取放入nuomi_shop_download_url.txt 文件
* 根据需要设定 DEPTH_LIMIT 爬去深度，原则上不要大于2
* 每次爬去后新增的地址放入相应配置文件