import feedparser
import time
import os
import re


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

    insert_info = "---start---\n\n## 最近更新文章(" + time.strftime('%Y年%m月%d日') + "更新)" +"\n" + insert_info + "\n---end---"

    # 获取README.md内容
    with open (os.path.join(os.getcwd(), "README.md"), 'r', encoding='utf-8') as f:
        readme_md_content = f.read()

    print(insert_info)

    new_readme_md_content = re.sub(r'---start---(.|\n)*---end---', insert_info, readme_md_content)

    with open (os.path.join(os.getcwd(), "README.md"), 'w', encoding='utf-8') as f:
        f.write(new_readme_md_content)



main()