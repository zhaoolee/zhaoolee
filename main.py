import feedparser
import time
import os
import re
import pytz
from datetime import datetime

def get_link_info(feed_url, num):

    result = ""
    feed = feedparser.parse(feed_url)
    feed_entries = feed["entries"]
    feed_entries_length = len(feed_entries)
    all_number = 0;

    if(num > feed_entries_length):
        all_number = feed_entries_length
    else:
        all_number = num
    
    for entrie in feed_entries[0: all_number]:
        title = entrie["title"]
        link = entrie["link"]
        result = result + "\n" + "[" + title + "](" + link + ")" + "\n"
    
    return result
    








def main():


    
    v2fy_info =  get_link_info("https://v2fy.com/feed/", 3)
    print(v2fy_info)
    fangyuanxiaozhan_info =  get_link_info("https://fangyuanxiaozhan.com/feed/", 3)
    print(fangyuanxiaozhan_info)

    insert_info = v2fy_info + fangyuanxiaozhan_info

    # 替换 ---start--- 到 ---end--- 之间的内容
    # pytz.timezone('Asia/Shanghai')).strftime('%Y年%m月%d日%H时M分')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    insert_info = "---start---\n\n## zhaoolee（老法师昭昭）的每日更新(" + "更新时间:"+  datetime.fromtimestamp(int(time.time()),pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') + " | 本部分通过Github Actions抓取RSS自动更新, 无意中实现了自动刷绿墙...)" +"\n" + insert_info + "\n---end---"
    # 获取README.md内容
    with open (os.path.join(os.getcwd(), "README.md"), 'r', encoding='utf-8') as f:
        readme_md_content = f.read()

    print(insert_info)

    new_readme_md_content = re.sub(r'---start---(.|\n)*---end---', insert_info, readme_md_content)

    with open (os.path.join(os.getcwd(), "README.md"), 'w', encoding='utf-8') as f:
        f.write(new_readme_md_content)



main()
