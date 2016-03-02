# 美食爬取

## 点评网爬取注意事项
    点评网采用了反爬取机制。在全量爬取时，需要通过不断变更ＩＰ来爬取．在每次爬去结束后需要检查../hlwdata/data/page/pageindex.txt
    中是否有403报错的文件。并提取出来放入dianping_start_url.txt 重新爬取
### 点评网后台处理脚本
    cd /home/sponge/scrapy/hlwdata
    grep 403 ./log/scrapy.dianping.log  | grep "Ignoring response" | awk '{print $8}' | awk -F ">" '{print $1}' |sort -u > ./data/url/dianping_start_url.txt
    python ../foods/foods/utils/comm.py
    grep "not meishi" ./log/scrapy.dianping.log   | awk '{print $3}' >> ./data/url/dianping_download_url.txt
    awk -F "," '{printf "https://www.dianping.com/shop/%s\n", $1}' ./data/dianping_new.csv  | sort -u >> ./data/url/dianping_download_url.txt 
    cd /home/sponge/scrapy/foods
    nohup python main.py dianping > ../hlwdata/log/scrapy.dianping.log &

 
## 软件操作流程

    进入根目录
    cd /home/sponge/scrapy/hlwdata
    export PYTHONPATH=/home/scrapy/liuhb/foods
    runscrapy.sh
### 提取最后一个字段
    临时行调用comm extractUrl(sys.argv[1]) 函数提取url
    python ../../foods/foods/utils/comm.py ./nuomi_new_page.csv  > ./url/nuomi_shop_download_url
    python ../../foods/foods/utils/comm.py ./meituan_new_page.csv > ./url/meituan_download_url.txt
    python ../../foods/foods/utils/comm.py ./dianping_new_page.csv  > ./url/dianping_download_url.txt
     
### 运行文件分析
    服务器上运行时需要加入模块路径 
    进入数据目录构造相应的爬取文件索引 dianping_page_index.txt meituan_page_index.txt
    cd /home/scrapy/liuhb/foods
    export PYTHONPATH=/home/scrapy/liuhb/foods
    python  foods/utils/spider/dianping.py