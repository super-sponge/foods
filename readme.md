明天开发点评数据

foods  include meituan runing 


ls | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/cq.meituan.com/%s\n",$1 }' > ../../url/meituan_page_index.txt
 
 
ls | grep "/shop." | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/www.nuomi.com/%s\n",$1 }' > ../../url/nuomi_page_index.txt

ls | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/%s\n",$1 }' > ../../url/dianping_page_index.txt
 

软件操作流程

进入根目录

python main.py dianping



#点评程序从跑脚本

cd /home/sponge/scrapy/hlwdata

grep 403 ./log/scrapy.dianping.log  | grep "Ignoring response" | awk '{print $8}' | awk -F ">" '{print $1}' |sort -u > ./data/url/dianping_start_url.txt

python ../foods/foods/utils/comm.py

grep "not meishi" ./log/scrapy.dianping.log   | awk '{print $3}' >> ./data/url/dianping_download_url.txt
awk -F "," '{printf "https://www.dianping.com/shop/%s\n", $1}' ./data/dianping_new.csv  | sort -u >> ./data/url/dianping_download_url.txt 

cd /home/sponge/scrapy/foods
nohup python main.py dianping > ../hlwdata/log/scrapy.dianping.log &


临时行调用comm extractUrl(sys.argv[1]) 函数提取url
 python ../../foods/foods/utils/comm.py ./nuomi_new_page.csv  > ./url/nuomi_shop_download_url
 python ../../foods/foods/utils/comm.py ./meituan_new_page.csv > ./url/meituan_download_url.txt
 python ../../foods/foods/utils/comm.py ./dianping_new_page.csv  > ./url/dianping_download_url.txt
 
 
 下周工作：
 
 a)编写清理下载的错误文件
 b)在糯米和点评spider中添加判断重庆的语句
 c)编写拨号程序，解决点评网数据爬取问题
 
 糯米多了 shop_shen
 
 
服务器上运行时需要加入模块路径    
cd /home/scrapy/liuhb/foods
export PYTHONPATH=/home/scrapy/liuhb/foods
python  foods/utils/spider/dianping.py