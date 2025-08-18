import feedparser
import os
import re
from datetime import datetime
import pytz

def get_link_info(feed_url, num):
    feed = feedparser.parse(feed_url)
    entries = feed.entries[:num]
    return "\n".join(f"- [{entry.title}]({entry.link})" for entry in entries)

def update_readme(insert_info):
    readme_path = os.path.join(os.getcwd(), "README.md")
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    update_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    insert_info = f"""---start---

## zhaoolee（老法师昭昭）的每日更新

> 更新时间: {update_time} | 本部分通过Github Actions抓取RSS自动更新，无意中实现了自动刷绿墙...

{insert_info}

---end---"""

    new_content = re.sub(r'---start---(.|\n)*---end---', insert_info, content)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return insert_info

def main():
    RSSHUB_ACCESS_KEY = os.getenv("RSSHUB_ACCESS_KEY")
    if not RSSHUB_ACCESS_KEY:
        raise RuntimeError("RSSHUB_ACCESS_KEY 未注入到环境变量（请在 workflow 的 env 中传入 secrets）")

    feeds = [
        ("https://v2fy.com/feed/?allow=zhaoolee", 3),
        ("https://fangyuanxiaozhan.com/feed/", 3),
        (f"https://rsshub.v2fy.com/xiaohongshu/user/566a6d770bf90c7076c1f397/notes?key={RSSHUB_ACCESS_KEY}", 6),
    ]
    
    all_info = []
    for url, num in feeds:
        feed_info = get_link_info(url, num)
        all_info.append(feed_info)
        print(f"\n获取到的信息：\n{feed_info}\n")

    insert_info = "\n\n".join(all_info)
    
    final_result = update_readme(insert_info)
    print("\n最终更新到 README.md 的内容：\n")
    print(final_result)

if __name__ == "__main__":
    main()
