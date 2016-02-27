明天开发点评数据

foods  include meituan runing 


ls | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/cq.meituan.com/%s\n",$1 }' > ../../url/meituan_page_index.txt
 
 
ls | grep "/shop." | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/www.nuomi.com/%s\n",$1 }' > ../../url/nuomi_page_index.txt

ls | awk '{ printf "/home/sponge/scrapy/hlwdata/data/page/www.dianping.com/%s\n",$1 }' > ../../url/dianping_page_index.txt
 

软件操作流程

进入根目录

python main.py dianping



grep 403 main.dianping.py.log  | grep "Ignoring response" | awk '{print $8}' | awk -F ">" '{print $1}' > data/start_url.txt

python ./foods/utils/comm.py

grep "not meishi" main.dianping.py.log  | awk '{print $3}' >> ./data/downloaded_url.txt
awk -F "," '{print $1}' ./data/shopindex.csv | sort -u >>  ./data/downloaded_url.txt

nohup python main.py > main.dianping.py.log &
