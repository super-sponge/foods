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
    
# python 读取hbase

## thrift 读取hbase

### install thrift
    请参考 hbase 官方网站
    对于普通用户使用了自带的python ，需要进入thrift-0.9.3/lib/py 手动安装python的thrift 组件
### 拷贝hbase的thrift 配置文件
    对于用ambari + hdp 安装的hbase，其thrift在/usr/hdp/current/hbase-client/include/thrift目录下,启动thrift2 时拷贝hbase2.thrift
### 根据hbase2.thrift 生成python文件
    thrift -r --gen py hbase2.thrift
### 编写客服端程序
### 启动thrift server
    /usr/hdp/current/hbase-master/bin/hbase-daemon.sh start thrift2
## reset 读取hbase
